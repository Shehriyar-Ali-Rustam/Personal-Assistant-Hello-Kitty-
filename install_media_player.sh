#!/bin/bash
# Install media player for YouTube music playback

echo "Installing media player for music playback..."
echo ""

# Install mpv (best option)
echo "Installing mpv..."
sudo apt-get update
sudo apt-get install -y mpv

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ mpv installed successfully!"
    echo ""
    echo "You can now play music from YouTube!"
    echo "Try saying: 'Hello Kitty, play shape of you'"
else
    echo ""
    echo "⚠️  Installation failed. Try manually:"
    echo "   sudo apt-get install mpv"
fi
