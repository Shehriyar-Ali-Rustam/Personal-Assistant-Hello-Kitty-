# How to Use Hello Kitty Assistant

## Quick Start

### 1. Start the Assistant
```bash
bash start_assistant.sh
```

Or:
```bash
source venv/bin/activate
python hello_kitty_assistant.py
```

### 2. Talk to Hello Kitty

1. Wait for the message: **"Hello Kitty is now listening!"**
2. Say: **"Hello Kitty"**
3. Wait for response: **"Yes? How can I help you?"**
4. Ask your question!
5. Listen to the answer

### 3. Example Conversations

```
You: "Hello Kitty"
Assistant: "Yes? How can I help you?"
You: "What is your name?"
Assistant: "Hi there! I'm Hello Kitty, your friendly AI assistant..."

You: "Hello Kitty"
Assistant: "Yes? How can I help you?"
You: "Tell me a joke"
Assistant: "Of course! Here's a cute one for you! ..."
```

## Voice Commands

### Basic Commands:
- **"Hello Kitty"** - Wake up the assistant
- **"Goodbye"** / **"Exit"** / **"Quit"** - Stop the assistant
- **"Speak slower"** - Decrease speech speed
- **"Speak faster"** - Increase speech speed
- **"Normal speed"** - Reset to default speed
- **"Reset conversation"** - Clear conversation history

### Music Commands (NEW! 🎵):
- **"Play [song name]"** - Play a song from YouTube
- **"Stop music"** - Stop currently playing music
- **"Pause music"** - Pause the music

**Examples:**
- "Play shape of you"
- "Play lofi music"
- "Play Taylor Swift"

## Tips

- Speak clearly and at normal volume
- Wait for acknowledgment before asking your question
- The assistant remembers your conversation context
- ALSA audio warnings are normal and can be ignored

## Troubleshooting

**Microphone not working?**
- Check your microphone is connected
- Test with: `arecord -l`

**Wake word not detected?**
- Speak louder or closer to the microphone
- Try saying "hello kitty" more clearly
- Check background noise levels

**No speech output?**
- Check your speakers/headphones are connected
- Volume might be too low

## Configuration

Edit `.env` file to customize:
- `WAKE_WORD` - Change the activation phrase
- `VOICE_RATE` - Adjust speech speed (default: 150)
- `VOICE_VOLUME` - Adjust volume (0.0 to 1.0)
- `AI_PROVIDER` - Switch between 'gemini' or 'openai'

## Current Setup

- **AI Provider**: Gemini (Google)
- **Model**: gemini-2.5-flash
- **Wake Word**: "hello kitty"
- **Voice Rate**: 150 words per minute

---

**Enjoy your Hello Kitty Voice Assistant!** 🎀
