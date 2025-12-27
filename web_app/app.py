"""
Hello Kitty Web Chat Application
A web-based chat interface similar to ChatGPT/Gemini
"""

import os
import sys
import re
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
import json

# Add parent directory to path to import existing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_brain import AIBrain
from weather_time_module import WeatherTimeModule
from youtube_player import YouTubePlayer
from alarm_module import AlarmModule
from urdu_support import UrduSupport

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

# YouTube player for music
youtube_player = YouTubePlayer()

# Alarm module
def on_alarm_triggered(label):
    print(f"🔔 Alarm triggered: {label}")

alarm_module = AlarmModule(alarm_callback=on_alarm_triggered)

# Urdu language support
urdu_support = UrduSupport()


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
    """Handle special commands like weather, time, music, alarms, etc."""
    # Check for Urdu and translate if needed
    if urdu_support.detect_urdu(text):
        print(f"🇵🇰 Urdu detected: '{text}'")
        text = urdu_support.translate_to_english(text)

    text_lower = text.lower()

    # Music/YouTube commands - improved parsing
    if "play" in text_lower:
        song_query = text  # Use original text to preserve capitalization

        print(f"📝 Original input: '{text}'")

        # Remove play command and common filler words (case insensitive)
        song_query = re.sub(r'\bplay\b', '', song_query, flags=re.IGNORECASE).strip()
        song_query = re.sub(r'\bthe song\b', '', song_query, flags=re.IGNORECASE).strip()
        song_query = re.sub(r'\bon youtube\b', '', song_query, flags=re.IGNORECASE).strip()
        song_query = re.sub(r'\bfor me\b', '', song_query, flags=re.IGNORECASE).strip()
        song_query = re.sub(r'\bplease\b', '', song_query, flags=re.IGNORECASE).strip()
        song_query = re.sub(r'\bmusic\b', '', song_query, flags=re.IGNORECASE).strip()

        # Clean up extra spaces
        song_query = ' '.join(song_query.split())

        if song_query and len(song_query) > 1:
            print(f"🎵 Extracted song query: '{song_query}'")

            # Run YouTube search
            success, message = youtube_player.search_and_play(song_query)

            if success:
                return f"Playing {song_query} now! Say 'stop music' to stop."
            else:
                return f"Sorry, I couldn't find {song_query}. Please try a different song name."
        else:
            return "What song would you like me to play?"

    # Stop/pause music commands
    if youtube_player.is_playing_music():
        if "stop" in text_lower or "pause" in text_lower:
            print("✅ Stop command detected! Stopping music...")
            success, message = youtube_player.stop()
            if success:
                return "Music stopped."
            else:
                return "Stopping music."

    # If no music playing, require full phrase
    if "stop music" in text_lower or "stop the music" in text_lower or "pause music" in text_lower:
        success, message = youtube_player.stop()
        if success:
            return "Music stopped."
        else:
            return "No music is playing right now."

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

    # Alarm commands
    if "set alarm" in text_lower or "alarm lagao" in text_lower or ("set" in text_lower and "alarm" in text_lower):
        # Extract time from command (simple parsing)
        time_pattern = r'(\d{1,2}):(\d{2})|(\d{1,2})\s*(am|pm|a\.m\.|p\.m\.)'
        time_match = re.search(time_pattern, text_lower)

        if time_match:
            if time_match.group(1):  # HH:MM format
                alarm_time = f"{time_match.group(1)}:{time_match.group(2)}"
            else:  # Hour with AM/PM
                hour = time_match.group(3)
                period = time_match.group(4)
                alarm_time = f"{hour}:00"
                if 'pm' in period or 'p.m' in period:
                    alarm_time = f"{int(hour) + 12}:00"

            message = alarm_module.add_alarm(alarm_time, "Alarm")
            return message
        else:
            return "What time should I set the alarm for? Please say something like 'set alarm for 7:00 AM'."

    if "cancel alarm" in text_lower or "delete alarm" in text_lower:
        message = alarm_module.cancel_all_alarms()
        return message

    if ("show" in text_lower or "list" in text_lower or "my" in text_lower) and "alarm" in text_lower:
        message = alarm_module.get_alarms()
        return message

    # Reset conversation
    if "reset conversation" in text_lower or "clear history" in text_lower:
        ai_brain.reset_conversation()
        return "I've cleared our conversation history. Let's start fresh!"

    # Joke command
    if 'joke' in text_lower or 'funny' in text_lower:
        import random
        jokes = [
            "Why did the programmer quit? They didn't get arrays!",
            "What's a computer's favorite snack? Microchips!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
            "What do you call a cat that does magic tricks? A Hello Kitty-dabra!"
        ]
        return random.choice(jokes)

    # Help command
    if 'what can you do' in text_lower or 'help' in text_lower:
        return ("I can help you with lots of things! Try asking me to:\n"
                "• Play music (e.g., 'play shape of you')\n"
                "• Check the weather\n"
                "• Tell you the time or date\n"
                "• Set alarms\n"
                "• Tell jokes\n"
                "• Answer questions\n"
                "• Have a conversation!")

    return None


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  Hello Kitty Web Chat")
    print("=" * 60)
    print(f"  AI Provider: {ai_provider}")
    print(f"  Open in browser: http://localhost:5000")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
