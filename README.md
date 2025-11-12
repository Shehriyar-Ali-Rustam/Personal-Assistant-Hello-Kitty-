# Hello Kitty Voice Assistant

A voice-activated AI assistant similar to Alexa and Siri, powered by ChatGPT or Google Gemini. Say "Hello Kitty" to wake it up, ask your questions, and get intelligent spoken responses!

## Features

- **Wake Word Detection**: Activates when you say "Hello Kitty"
- **Speech Recognition**: Converts your voice to text using Google Speech Recognition
- **AI-Powered Responses**: Uses ChatGPT (OpenAI) or Gemini (Google) for intelligent answers
- **Text-to-Speech**: Speaks responses back to you in a natural voice
- **Conversation Memory**: Remembers context from your conversation
- **Customizable**: Configure wake word, voice speed, AI provider, and more

## System Requirements

- Python 3.8 or higher
- Microphone (built-in or external)
- Speakers/Headphones
- Internet connection (for speech recognition and AI services)
- Linux/Windows/macOS

## Installation

### Easy Installation (Recommended for Linux)

Run the automated setup script:
```bash
bash setup.sh
```

This will:
- Create a virtual environment
- Install system dependencies
- Install all Python packages
- Set everything up automatically

### Manual Installation

#### Step 1: Create Virtual Environment

**For Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### Step 2: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio espeak espeak-ng
```

**Fedora:**
```bash
sudo dnf install portaudio-devel python3-pyaudio espeak
```

**Arch:**
```bash
sudo pacman -S portaudio python-pyaudio espeak
```

**macOS:**
```bash
brew install portaudio
```

**Windows:** PyAudio installation may require [unofficial wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

#### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get API Keys

You need an API key from either OpenAI or Google:

#### Option A: OpenAI (ChatGPT)
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the API key

#### Option B: Google Gemini
1. Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### Step 5: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your API key:

**For OpenAI:**
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**For Gemini:**
```
AI_PROVIDER=gemini
GEMINI_API_KEY=your-actual-api-key-here
```

## Usage

### Start the Assistant

**Quick Run (if you used setup.sh):**
```bash
bash run.sh
```

**Or manually:**
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Run the assistant
python hello_kitty_assistant.py
```

### How to Interact

1. **Activate**: Say "Hello Kitty" (wait for the beep or acknowledgment)
2. **Ask**: Speak your question or command
3. **Listen**: Hello Kitty will respond with an answer
4. **Repeat**: Say "Hello Kitty" again for another question

### Example Conversation

```
You: "Hello Kitty"
Assistant: "Yes? How can I help you?"
You: "What's the weather like today?"
Assistant: "I don't have real-time weather data, but you can check..."

You: "Hello Kitty"
Assistant: "Yes? How can I help you?"
You: "Tell me a joke"
Assistant: "Why did the programmer quit his job? Because he didn't get arrays!"
```

### Special Commands

- **Exit**: Say "goodbye", "bye", "exit", or "quit" to stop the assistant
- **Reset conversation**: Say "reset conversation" or "clear history"
- **Adjust speed**: Say "speak slower", "speak faster", or "normal speed"

## Configuration Options

Edit the `.env` file to customize:

```env
# AI Provider (openai or gemini)
AI_PROVIDER=openai

# API Keys
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Wake word (what you say to activate)
WAKE_WORD=hello kitty

# Assistant name
ASSISTANT_NAME=Hello Kitty

# Voice settings
VOICE_RATE=150          # Speech speed (words per minute)
VOICE_VOLUME=0.9        # Volume (0.0 to 1.0)
```

## Troubleshooting

### Microphone Not Working
- Check microphone permissions
- Test microphone with other apps
- On Linux, check `pavucontrol` for input devices

### Speech Recognition Issues
- Ensure stable internet connection
- Speak clearly and at normal pace
- Reduce background noise
- Check microphone volume

### API Errors
- Verify API key is correct in `.env`
- Check API quota/credits
- Ensure internet connection is stable

### Installation Issues
- Make sure Python 3.8+ is installed: `python --version`
- Try upgrading pip: `pip install --upgrade pip`
- On Linux, install system audio libraries (see Step 2)

### "PyAudio" installation fails
**Windows**: Download and install from [unofficial wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
**Linux**: Install portaudio development package (see Step 2)
**macOS**: Install portaudio with Homebrew (see Step 2)

## Project Structure

```
Personal Assitant (Hello Kitty)/
├── hello_kitty_assistant.py    # Main application
├── wake_word_detector.py       # Wake word detection
├── speech_recognition_module.py # Speech-to-text
├── ai_brain.py                 # AI integration (ChatGPT/Gemini)
├── text_to_speech.py           # Text-to-speech
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment file
├── .env                       # Your API keys (create this)
└── README.md                  # This file
```

## Future Enhancements (Toy Deployment)

To deploy this on a Raspberry Pi or similar device for a toy:

1. **Hardware**: Raspberry Pi 4, USB microphone, speaker
2. **Auto-start**: Configure to run on boot
3. **Battery**: Add portable power supply
4. **Physical design**: 3D print Hello Kitty enclosure
5. **LED indicators**: Add visual feedback
6. **Offline mode**: Consider offline speech recognition

## License

This project is for educational and personal use.

## Credits

- Speech Recognition: Google Speech Recognition API
- AI: OpenAI GPT / Google Gemini
- Text-to-Speech: pyttsx3

---

**Enjoy your Hello Kitty Voice Assistant!** Say "Hello Kitty" to get started!
