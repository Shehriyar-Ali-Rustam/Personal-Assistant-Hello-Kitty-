# Voice Settings Guide

## Current Voice: Feminine Girl Voice

Your Hello Kitty assistant now uses a **feminine, girl-like voice** with higher pitch!

## How It Works

The assistant uses **espeak-ng** with special settings:
- **Higher pitch** (65 out of 99) - Makes it sound more feminine
- **Fast speech rate** (180 wpm) - Quick and responsive
- **Full volume** - Clear and easy to hear

## Voice Configuration

Edit `.env` file to customize:

### Feminine Voice (Current Setting)
```env
USE_FEMININE_VOICE=true
VOICE_PITCH=65
VOICE_RATE=180
VOICE_VOLUME=1.0
```

### Standard Voice (Neutral)
```env
USE_FEMININE_VOICE=false
VOICE_RATE=180
VOICE_VOLUME=1.0
```

## Pitch Settings

Adjust `VOICE_PITCH` for different femininity levels:
- `50` - Default (neutral)
- `60` - Slightly feminine
- `65` - Feminine (current)
- `70` - Very feminine
- `75` - Extra high pitch
- `80` - Maximum femininity

**Note**: Values range from 0-99

## Speed Settings

Adjust `VOICE_RATE` for speaking speed:
- `140` - Slower, more relaxed
- `160` - Moderate pace
- `180` - Fast and responsive (current)
- `200` - Very fast
- `220` - Maximum speed

## Volume Settings

Adjust `VOICE_VOLUME`:
- `0.7` - Quiet
- `0.9` - Normal
- `1.0` - Maximum (current)

## Test the Voice

After changing settings, test with:
```bash
source venv/bin/activate
python -c "
from text_to_speech import TextToSpeech
tts = TextToSpeech(rate=180, volume=1.0, use_espeak_female=True)
tts.speak('Hello! I am your Hello Kitty assistant!')
"
```

## Examples

### Very Feminine, Fast
```env
USE_FEMININE_VOICE=true
VOICE_PITCH=75
VOICE_RATE=200
```

### Moderate Feminine, Normal Speed
```env
USE_FEMININE_VOICE=true
VOICE_PITCH=60
VOICE_RATE=160
```

### Back to Neutral
```env
USE_FEMININE_VOICE=false
VOICE_RATE=150
```

---

**Your Hello Kitty assistant now has a cute, feminine voice!** 🎀
