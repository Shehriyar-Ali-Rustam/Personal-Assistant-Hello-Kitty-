# How to Use Hello Kitty Assistant

## Quick Start

### 1. Start the Assistant
```bash
bash run.sh
```

Or manually:
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

### Music Commands:
- **"Play [song name]"** - Play a song from YouTube
- **"Stop music"** - Stop currently playing music (works even without wake word!)
- **"Pause music"** - Pause the music

**Examples:**
- "Play shape of you"
- "Play lofi music"
- "Play Taylor Swift"

### Weather & Time Commands:
- **"What's the weather?"** - Get current weather in Karachi
- **"Weather in [city]"** - Get weather for any city
- **"What time is it?"** - Get current time
- **"What's the date?"** - Get current date

**Examples:**
- "What's the weather like?"
- "Weather in Lahore"
- "Tell me the time"

### Alarm Commands:
- **"Set alarm for [time]"** - Set an alarm (plays ringtone!)
- **"Set alarm [HH:MM]"** - Set alarm with specific time
- **"Show alarms"** / **"List alarms"** - View all alarms
- **"Delete alarm [number]"** - Remove an alarm

**Examples:**
- "Set alarm for 7:30 AM"
- "Set alarm 14:00"
- "Show my alarms"
- "Delete alarm 1"

### Multi-Language Support:
- **Urdu/Hindi** - Speak in Urdu (Roman or Urdu script) and it will be translated!

**Examples:**
- "Mausam kaisa hai?" (How's the weather?)
- "Waqt kya hua?" (What time is it?)

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
- `WAKE_WORD` - Change the activation phrase (default: "hello kitty")
- `VOICE_RATE` - Adjust speech speed (default: 150)
- `VOICE_VOLUME` - Adjust volume (0.0 to 1.0)
- `AI_PROVIDER` - Switch between 'openai' or 'gemini'
- `CITY` - Default city for weather (default: Karachi)
- `TIMEZONE` - Your timezone (default: Asia/Karachi)

## Current Setup

- **AI Provider**: OpenAI (GPT-3.5-turbo)
- **Wake Word**: "hello kitty"
- **Voice Rate**: 150 words per minute
- **Features**: Music Player, Weather & Time, Alarms with Ringtone, Urdu Support

---

**Enjoy your Hello Kitty Voice Assistant!** 🎀
