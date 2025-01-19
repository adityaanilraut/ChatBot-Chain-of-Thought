# app.py
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI

import time
from typing import List
import statistics
from difflib import SequenceMatcher
from datetime import datetime
import os

api_key = os.getenv('API_KEY')  # Retrieve the API key from environment variables
if not api_key:
    raise ValueError("API Key not found. Please set the API_KEY environment variable.")

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

def moderate_content(content: str) -> tuple[bool, dict]:
    """Uses OpenAI's Moderation API to check content for harmful material."""
    try:
        response = llm_handler.client.moderations.create(input=content)
        results = response.results[0]
        flagged = results.flagged
        categories = results.categories
        return flagged, categories
    except Exception as e:
        print(f"Error during moderation: {e}")
        return False, {}

class LLMHandler:
    def __init__(self, base_url: str = "https://api.openai.com/v1/", api_key: str = api_key):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def get_response(self, prompt: str, conversation_history: List[dict], 
                    temperature: float = 0.7, use_cot: bool = False) -> str:
        """Get a single response from the LLM."""
        system_prompt = (
            "You are a helpful assistant. "
            "When answering, first break down the problem into steps, "
            "then provide your reasoning for each step, "
            "and finally give your conclusion."
        ) if use_cot else "You are a helpful assistant."
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history,
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_multiple_responses(self, prompt: str, conversation_history: List[dict], 
                             use_cot: bool = False) -> List[str]:
        """Generate multiple responses for comparison."""
        responses = []
        temperatures = [0.3, 0.5, 0.7]
        
        for temp in temperatures:
            response = self.get_response(prompt, conversation_history, temp, use_cot)
            responses.append(response)
            time.sleep(1)
        
        return responses
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def get_best_response(self, responses: List[str]) -> str:
        """Select the best response based on similarity."""
        if len(responses) == 1:
            return responses[0]
        
        similarity_scores = []
        for i, resp1 in enumerate(responses):
            avg_similarity = statistics.mean(
                self.calculate_similarity(resp1, resp2)
                for j, resp2 in enumerate(responses)
                if i != j
            )
            similarity_scores.append((avg_similarity, i))
        
        best_idx = max(similarity_scores, key=lambda x: x[0])[1]
        return responses[best_idx]

# Initialize LLM handler
llm_handler = LLMHandler()

@app.route('/')
def home():
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html', conversation=session['conversation'])

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '').strip()
    use_cot = data.get('use_cot', False)
    compare_responses = data.get('compare_responses', True)
    temperature = float(data.get('temperature', 0.7))
    
    if not message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Check content moderation before processing
    flagged, categories = moderate_content(message)
    if flagged:
        return jsonify({
            'error': 'Message flagged by content moderation',
            'categories': categories
        }), 400
    
    # Add user message to conversation
    timestamp = datetime.now().strftime("%H:%M")
    session['conversation'] = session.get('conversation', [])
    session['conversation'].append({
        'role': 'user',
        'content': message,
        'timestamp': timestamp
    })
    
    # Get bot response
    if compare_responses:
        responses = llm_handler.get_multiple_responses(
            message, 
            session['conversation'],
            use_cot
        )
        response = llm_handler.get_best_response(responses)
    else:
        response = llm_handler.get_response(
            message,
            session['conversation'],
            temperature,
            use_cot
        )
    
    # Moderate bot response before sending
    flagged, categories = moderate_content(response)
    if flagged:
        response = "I apologize, but I cannot provide that response as it may contain inappropriate content."
    
    # Add bot response to conversation
    session['conversation'].append({
        'role': 'assistant',
        'content': response,
        'timestamp': timestamp
    })
    session.modified = True
    
    return jsonify({
        'response': response,
        'timestamp': timestamp
    })

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    session['conversation'] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)