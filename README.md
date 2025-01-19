# Aditya's LLM Chatbot 🤖

A sleek, interactive chatbot interface that supports chain-of-thought reasoning and response comparison. Built with Python Flask and modern web technologies, this chatbot can work with various LLM backends including Open AI's o1-mini models.

## 🌟 Features

- Clean, modern interface built with Tailwind CSS
- Real-time response streaming with typing animation
- Chain of Thought (CoT) reasoning toggle
- Response comparison mode
- Adjustable temperature settings
- Sample prompts for quick testing
- Mobile-responsive design

## 🛠️ Tech Stack

- **Frontend**: HTML, TailwindCSS, JavaScript
- **Backend**: Python Flask
- **LLM Integration**: Open AI API (default) / Ollama / LM Studio
- **Default Model**: o1-mini (via Open AI)

## 📁 Project Structure

```
llm-chatbot/
│
├── app.py                 # Flask application server
├── templates/
│   └── index.html        # Main chat interface
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-chatbot.git
cd llm-chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
```bash
# For Open AI
export Open_API_KEY=your_api_key_here

# For local setup (Ollama/LM Studio)
# No API key needed
```

## 🚀 Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## 🔄 Chain of Thought (CoT) Explained

Chain of Thought is a prompting technique that enables the LLM to break down complex problems into steps and show its reasoning process. When enabled:

1. The model explains its thought process step by step
2. Shows intermediate reasoning before reaching conclusions
3. Provides more transparent and verifiable responses

Example CoT response:
```
Question: What is 15% of 80?

Thinking:
1. To find a percentage, I need to convert 15% to decimal (15/100 = 0.15)
2. Then multiply 80 by 0.15
3. 80 × 0.15 = 12

Answer: 15% of 80 is 12
```

## 💰 Cost Considerations

### Open AI (o1-mini)
- Input tokens: $0.150 / 1M tokens
- Output tokens: $0.600 / 1M tokens
- Chain of Thought and Compare Responses can use up to 3x more tokens
- Recommended to monitor token usage carefully

### Local Alternatives
- **Ollama**: Free, runs locally
  - Supports various open-source models
  - Lower resource requirements
  - Setup guide: [Ollama Documentation](https://ollama.ai)

- **LM Studio**: Free, runs locally
  - Supports multiple open-source models
  - User-friendly interface
  - Setup guide: [LM Studio Documentation](https://lmstudio.ai)

## 🔧 Backend Configuration

### Open AI Setup
```python
# In app.py
Open_API_KEY = os.getenv('Open_API_KEY')
API_URL = "https://api.openai.com/v1/"
```

### Local Setup (Ollama)
```python
# In app.py
API_URL = "http://localhost:11434/api/generate"
MODEL = "gpt-4o-mini"  # or any other model you've pulled
```

### LM Studio Setup
```python
# In app.py
API_URL = "http://localhost:1234/v1/chat/completions"  # Default LM Studio endpoint
```

## ⚙️ Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| Temperature | Controls response randomness | 0.7 |
| Chain of Thought | Enables step-by-step reasoning | On |
| Compare Responses | Generates multiple responses | On |

## 🚨 Important Notes

1. **Token Usage**: 
   - CoT and Compare Responses features can triple token usage
   - Clear chat regularly to manage token consumption
   - Monitor API costs when using Open AI

2. **Local Deployment**:
   - Use Ollama or LM Studio for free local testing
   - Requires sufficient RAM and CPU/GPU resources
   - Performance varies based on hardware

3. **API Keys**:
   - Keep API keys secure
   - Don't commit keys to version control
   - Use environment variables for key management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Acknowledgments

- Open AI for the o1-mini model
- Tailwind CSS for styling utilities
- Flask community for the web framework
