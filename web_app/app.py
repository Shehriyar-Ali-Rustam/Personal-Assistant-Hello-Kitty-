"""
Hello Kitty Web Chat Application
A web-based chat interface similar to ChatGPT/Gemini
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
import json

# Add parent directory to path to import existing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_brain import AIBrain
from weather_time_module import WeatherTimeModule

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

app = Flask(__name__)
CORS(app)

# Initialize AI Brain
ai_provider = os.getenv("AI_PROVIDER", "openai").lower()
if ai_provider == "openai":
    api_key = os.getenv("OPENAI_API_KEY")
elif ai_provider == "gemini":
    api_key = os.getenv("GEMINI_API_KEY")
else:
    raise ValueError(f"Unknown AI provider: {ai_provider}")

ai_brain = AIBrain(provider=ai_provider, api_key=api_key)

# Weather/Time module
city = os.getenv("CITY", "Karachi")
timezone = os.getenv("TIMEZONE", "Asia/Karachi")
weather_time = WeatherTimeModule(city=city, timezone=timezone)


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Check for special commands
    response = handle_special_commands(user_message)

    if response is None:
        # Get AI response
        response = ai_brain.get_response(user_message)

    return jsonify({
        'response': response,
        'status': 'success'
    })


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Handle chat messages with streaming response (like ChatGPT)"""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Check for special commands first
    special_response = handle_special_commands(user_message)

    if special_response:
        # For special commands, return immediately
        def generate_special():
            yield f"data: {json.dumps({'content': special_response, 'done': True})}\n\n"
        return Response(generate_special(), mimetype='text/event-stream')

    # Stream AI response
    def generate():
        try:
            response = ai_brain.get_response(user_message)
            # Simulate streaming by sending word by word
            words = response.split()
            for i, word in enumerate(words):
                chunk = word + (' ' if i < len(words) - 1 else '')
                yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"
            yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"

    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    ai_brain.reset_conversation()
    return jsonify({'status': 'success', 'message': 'Conversation reset'})


@app.route('/api/status', methods=['GET'])
def status():
    """Get API status"""
    return jsonify({
        'status': 'online',
        'provider': ai_provider,
        'conversation_count': ai_brain.get_conversation_count()
    })


def handle_special_commands(text):
    """Handle special commands like weather, time, etc."""
    text_lower = text.lower()

    # Weather commands
    if 'weather' in text_lower or 'mausam' in text_lower:
        return weather_time.get_weather()

    # Time commands
    if ('time' in text_lower and 'what' in text_lower) or 'waqt' in text_lower:
        return f"The current time is {weather_time.get_current_time()}"

    # Date commands
    if ('date' in text_lower and ('what' in text_lower or 'today' in text_lower)) or 'tareekh' in text_lower:
        return f"Today is {weather_time.get_current_date()}"

    # Day commands
    if 'what day' in text_lower or 'which day' in text_lower or 'aaj kya din' in text_lower:
        return f"Today is {weather_time.get_day_of_week()}"

    return None


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  Hello Kitty Web Chat")
    print("=" * 60)
    print(f"  AI Provider: {ai_provider}")
    print(f"  Open in browser: http://localhost:5000")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
