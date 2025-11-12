# 🎵 YouTube Music Playback

Your Hello Kitty assistant can now **play music from YouTube**!

## How to Use

### Play a Song

Say: **"Hello Kitty"**
Then: **"Play [song name]"**

### Examples:

- "Play shape of you"
- "Play Billie Eilish bad guy"
- "Play Taylor Swift shake it off"
- "Play lofi music"
- "Play relaxing music"

### Stop Music

Say: **"Hello Kitty"**
Then: **"Stop music"**

## Installation Requirements

For YouTube playback to work, you need a media player installed.

### Install mpv (Recommended):
```bash
sudo apt-get install mpv
```

### Or install ffmpeg:
```bash
sudo apt-get install ffmpeg
```

### Or install VLC:
```bash
sudo apt-get install vlc
```

## How It Works

1. You ask Hello Kitty to play a song
2. She searches YouTube for the song
3. Finds the first/best result
4. Plays the audio (without video)
5. Music plays in the background

## Voice Commands

| Command | What it does |
|---------|-------------|
| "Play [song name]" | Plays the song from YouTube |
| "Play music" | Asks what song you want |
| "Stop music" | Stops currently playing music |
| "Pause music" | Stops the music |

## Examples of What to Say:

```
You: "Hello Kitty"
Assistant: "Yes? How can I help you?"
You: "Play Shape of You by Ed Sheeran"
Assistant: "Okay! Searching for shape of you ed sheeran on YouTube."
[Song starts playing]
Assistant: "Music is now playing! Say stop music to stop."
```

```
You: "Hello Kitty"
Assistant: "Yes? How can I help you?"
You: "Stop music"
Assistant: "Music stopped."
```

## Features

- ✅ Searches YouTube automatically
- ✅ Plays audio only (no video window)
- ✅ Works with any song on YouTube
- ✅ Natural voice commands
- ✅ Easy to stop/pause

## Troubleshooting

**"No media player found" error:**
- Install mpv: `sudo apt-get install mpv`

**Song not playing:**
- Check internet connection
- Make sure YouTube isn't blocked
- Try a different song name

**Song not found:**
- Try being more specific
- Include artist name
- Use the full song title

---

**Enjoy your music with Hello Kitty!** 🎵🎀
