"""
Hello Kitty Voice Assistant
Main application that ties all modules together
"""
import os
import time
from dotenv import load_dotenv
from wake_word_detector import WakeWordDetector
from speech_recognition_module import SpeechRecognizer
from ai_brain import AIBrain
from text_to_speech import TextToSpeech
from youtube_player import YouTubePlayer


class HelloKittyAssistant:
    def __init__(self):
        """Initialize the Hello Kitty Assistant"""
        print("=" * 60)
        print("🎀 HELLO KITTY VOICE ASSISTANT 🎀")
        print("=" * 60)

        # Load environment variables
        load_dotenv()

        # Get configuration from environment
        self.ai_provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.wake_word = os.getenv("WAKE_WORD", "hello kitty")
        self.assistant_name = os.getenv("ASSISTANT_NAME", "Hello Kitty")

        # Get API key based on provider
        if self.ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in .env file")
        elif self.ai_provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in .env file")
        else:
            raise ValueError(f"Unknown AI provider: {self.ai_provider}")

        # Initialize components
        print("\n🔧 Initializing components...")
        self.wake_detector = WakeWordDetector([self.wake_word])
        self.speech_recognizer = SpeechRecognizer()
        self.ai_brain = AIBrain(provider=self.ai_provider, api_key=api_key)

        # Text-to-speech settings
        voice_rate = int(os.getenv("VOICE_RATE", "180"))
        voice_volume = float(os.getenv("VOICE_VOLUME", "1.0"))
        use_google = os.getenv("USE_GOOGLE_TTS", "true").lower() == "true"
        self.tts = TextToSpeech(rate=voice_rate, volume=voice_volume, use_google_tts=use_google)

        # YouTube music player
        self.youtube_player = YouTubePlayer()

        self.is_active = False
        self.running = True

        print("\n✅ All components initialized successfully!")

    def on_wake_word_detected(self):
        """Called when wake word is detected"""
        if self.is_active:
            return  # Already processing a request

        self.is_active = True

        # Acknowledge wake word
        self.tts.speak("Yes? How can I help you?")

        # Listen for user's question - longer time for music commands
        user_input = self.speech_recognizer.listen(timeout=10, phrase_time_limit=20)

        if user_input:
            # Check for exit commands
            if self._is_exit_command(user_input):
                self.tts.speak("Goodbye! Have a wonderful day!")
                self.running = False
                self.is_active = False
                return

            # Check for special commands
            if self._handle_special_commands(user_input):
                self.is_active = False
                return

            # Get AI response
            print("\n🤖 Thinking...")
            response = self.ai_brain.get_response(user_input)

            # Speak the response
            self.tts.speak(response)
        else:
            self.tts.speak("I didn't catch that. Please say the wake word again.")

        self.is_active = False

    def _is_exit_command(self, text):
        """Check if user wants to exit"""
        exit_phrases = ["goodbye", "bye", "exit", "quit", "stop", "shutdown"]
        return any(phrase in text.lower() for phrase in exit_phrases)

    def _handle_special_commands(self, text):
        """Handle special assistant commands"""
        text_lower = text.lower()

        # Music commands - improved parsing
        if "play" in text_lower:
            # Better song extraction
            song_query = text_lower

            # Remove play command and common words
            song_query = song_query.replace("play", "").strip()
            song_query = song_query.replace("the song", "").strip()
            song_query = song_query.replace("song", "").strip()
            song_query = song_query.replace("music", "").strip()
            song_query = song_query.replace("on youtube", "").strip()
            song_query = song_query.replace("youtube", "").strip()
            song_query = song_query.replace("for me", "").strip()
            song_query = song_query.replace("please", "").strip()

            # Remove extra articles
            if song_query.startswith("the "):
                song_query = song_query[4:]
            if song_query.startswith("a "):
                song_query = song_query[2:]

            song_query = song_query.strip()

            if song_query and len(song_query) > 2:
                print(f"🎵 Extracted song query: '{song_query}'")
                self.tts.speak(f"Searching for {song_query}")

                # Run YouTube search in background to avoid blocking
                success, message = self.youtube_player.search_and_play(song_query)

                if success:
                    self.tts.speak("Playing now! Say stop music to stop.")
                else:
                    self.tts.speak(f"Sorry, couldn't find {song_query}. Try again?")
                return True
            else:
                self.tts.speak("What song would you like to hear?")
                return True

        if "stop music" in text_lower or "stop the music" in text_lower or "pause music" in text_lower:
            success, message = self.youtube_player.stop()
            if success:
                self.tts.speak("Music stopped.")
            else:
                self.tts.speak("No music is playing.")
            return True

        # Reset conversation
        if "reset conversation" in text_lower or "clear history" in text_lower:
            self.ai_brain.reset_conversation()
            self.tts.speak("I've cleared our conversation history.")
            return True

        # Change voice rate
        if "speak slower" in text_lower:
            self.tts.set_rate(120)
            self.tts.speak("Okay, I'll speak slower.")
            return True

        if "speak faster" in text_lower:
            self.tts.set_rate(180)
            self.tts.speak("Okay, I'll speak faster.")
            return True

        if "normal speed" in text_lower:
            self.tts.set_rate(150)
            self.tts.speak("Back to normal speed.")
            return True

        return False

    def run(self):
        """Start the assistant"""
        try:
            print("\n" + "=" * 60)
            print(f"👂 {self.assistant_name} is now listening!")
            print(f"🎤 Say '{self.wake_word}' to activate")
            print("🛑 Say 'goodbye' or 'exit' to stop the assistant")
            print("=" * 60 + "\n")

            # Start wake word detection
            self.wake_detector.start(self.on_wake_word_detected)

            # Keep the main thread alive
            while self.running:
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted by user")
        finally:
            self.shutdown()

    def shutdown(self):
        """Clean shutdown"""
        print("\n🔴 Shutting down Hello Kitty Assistant...")
        self.wake_detector.stop()
        print("👋 Goodbye!")


def main():
    """Main entry point"""
    try:
        assistant = HelloKittyAssistant()
        assistant.run()
    except Exception as e:
        print(f"\n❌ Error starting assistant: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Created a .env file with your API keys")
        print("   2. Installed all requirements: pip install -r requirements.txt")
        print("   3. A working microphone connected")


if __name__ == "__main__":
    main()
