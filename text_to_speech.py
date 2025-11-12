"""
Text-to-Speech Module
Converts text responses to spoken audio
Uses Google TTS for high-quality, natural female voice
"""
import pyttsx3
import subprocess
import os
from gtts import gTTS
import pygame
import tempfile
import time


class TextToSpeech:
    def __init__(self, rate=180, volume=1.0, use_google_tts=True):
        """
        Initialize text-to-speech engine

        Args:
            rate: Speech rate (only for pyttsx3, gTTS is naturally fast)
            volume: Volume level (0.0 to 1.0)
            use_google_tts: Use Google TTS for natural female voice (recommended)
        """
        self.use_google_tts = use_google_tts
        self.rate = rate
        self.volume = volume

        if use_google_tts:
            # Initialize pygame mixer for audio playback
            try:
                pygame.mixer.init()
                self.engine = None
                print("✓ Text-to-Speech initialized with Google TTS (natural female voice)")
            except Exception as e:
                print(f"⚠️  Pygame mixer failed: {e}, falling back to pyttsx3")
                self.use_google_tts = False
                self._init_pyttsx3()
        else:
            self._init_pyttsx3()

    def _init_pyttsx3(self):
        """Initialize pyttsx3 as fallback"""
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')

        # Try to find best English voice
        voice_preferences = ['gmw/en-us', 'gmw/en-gb-x-rp', 'gmw/en', 'gmw/en-gb']
        for pref in voice_preferences:
            for voice in voices:
                if pref in voice.id:
                    self.engine.setProperty('voice', voice.id)
                    break

        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        print("✓ Text-to-Speech initialized with pyttsx3")

    def speak(self, text):
        """
        Convert text to speech and play it

        Args:
            text: Text to speak
        """
        print(f"\n💬 Hello Kitty: {text}")

        try:
            if self.use_google_tts:
                # Use Google TTS - natural female voice
                # Create temporary file for audio
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name

                # Generate speech with Google TTS
                # Using 'en' (English) with default settings gives a nice female voice
                # For more feminine: can try 'en-gb', 'en-us', 'en-au'
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_file)

                # Play the audio
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()

                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                # Clean up temporary file
                try:
                    os.unlink(temp_file)
                except:
                    pass

            else:
                # Use pyttsx3 fallback
                self.engine.say(text)
                self.engine.runAndWait()

        except Exception as e:
            print(f"❌ Error in text-to-speech: {e}")
            # Try fallback
            if self.use_google_tts and self.engine is None:
                print("Falling back to pyttsx3...")
                self._init_pyttsx3()
                self.use_google_tts = False
                self.speak(text)

    def set_rate(self, rate):
        """Set speech rate (only affects pyttsx3)"""
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = volume
        if self.engine:
            self.engine.setProperty('volume', volume)

    def list_voices(self):
        """List available voices (pyttsx3 only)"""
        if self.engine:
            voices = self.engine.getProperty('voices')
            print("\nAvailable voices:")
            for idx, voice in enumerate(voices):
                print(f"{idx}: {voice.name} - {voice.id}")
            return voices
        else:
            print("Using Google TTS - no voice selection needed")
            return []

    def set_voice(self, voice_id):
        """Set voice by ID (pyttsx3 only)"""
        if self.engine:
            self.engine.setProperty('voice', voice_id)

    def __del__(self):
        """Cleanup"""
        if self.use_google_tts:
            try:
                pygame.mixer.quit()
            except:
                pass
