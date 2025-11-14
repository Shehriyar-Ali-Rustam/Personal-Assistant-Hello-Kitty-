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
from weather_time_module import WeatherTimeModule
from alarm_module import AlarmModule
from urdu_support import UrduSupport


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

        # Weather and Time module
        city = os.getenv("CITY", "Karachi")
        timezone = os.getenv("TIMEZONE", "Asia/Karachi")
        self.weather_time = WeatherTimeModule(city=city, timezone=timezone)

        # Alarm module with callback
        self.alarm_module = AlarmModule(alarm_callback=self.on_alarm_triggered)

        # Urdu language support
        self.urdu_support = UrduSupport()

        self.is_active = False
        self.running = True

        print("\n✅ All components initialized successfully!")

    def on_alarm_triggered(self, label):
        """Called when an alarm goes off"""
        print(f"🔔 Alarm triggered: {label}")
        self.tts.speak(f"Alarm! {label}")

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
            # Check for Urdu and translate if needed
            if self.urdu_support.detect_urdu(user_input):
                print(f"🇵🇰 Urdu detected: '{user_input}'")
                user_input = self.urdu_support.translate_to_english(user_input)
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
        text_lower = text.lower()
        # Don't exit if they're trying to stop music
        if "stop music" in text_lower or "stop the music" in text_lower:
            return False
        # Don't exit if music is playing and they say "stop" (they mean stop music)
        if self.youtube_player.is_playing_music() and "stop" in text_lower:
            return False
        exit_phrases = ["goodbye", "bye", "exit", "quit", "shutdown"]
        return any(phrase in text_lower for phrase in exit_phrases)

    def _handle_special_commands(self, text):
        """Handle special assistant commands"""
        text_lower = text.lower()

        # Music commands - improved parsing
        if "play" in text_lower:
            # Better song extraction - preserve original case for song names
            song_query = text  # Use original text to preserve capitalization

            # Log what was heard
            print(f"📝 Original input: '{text}'")

            # Remove play command and common filler words (case insensitive)
            import re
            # Remove "play" and common phrases
            song_query = re.sub(r'\bplay\b', '', song_query, flags=re.IGNORECASE).strip()
            song_query = re.sub(r'\bthe song\b', '', song_query, flags=re.IGNORECASE).strip()
            song_query = re.sub(r'\bon youtube\b', '', song_query, flags=re.IGNORECASE).strip()
            song_query = re.sub(r'\bfor me\b', '', song_query, flags=re.IGNORECASE).strip()
            song_query = re.sub(r'\bplease\b', '', song_query, flags=re.IGNORECASE).strip()

            # Clean up extra spaces
            song_query = ' '.join(song_query.split())

            if song_query and len(song_query) > 1:
                print(f"🎵 Extracted song query: '{song_query}'")
                self.tts.speak(f"Searching for {song_query}")

                # Run YouTube search
                success, message = self.youtube_player.search_and_play(song_query)

                if success:
                    self.tts.speak("Playing now! Say stop music to stop.")
                else:
                    self.tts.speak(f"Sorry, I couldn't find {song_query}. Try saying it again?")
                return True
            else:
                self.tts.speak("What song would you like to hear?")
                return True

        # Check for stop/pause music commands
        # If music is playing, just "stop" is enough (easier to hear over music)
        if self.youtube_player.is_playing_music():
            print(f"🎵 Music is currently playing. Checking for stop command in: '{text}'")
            if "stop" in text_lower or "pause" in text_lower:
                print("✅ Stop command detected! Stopping music...")
                success, message = self.youtube_player.stop()
                if success:
                    self.tts.speak("Music stopped.")
                else:
                    self.tts.speak("Stopping music.")
                return True
            else:
                print(f"   No stop command found in '{text}'")

        # If no music playing, require full phrase
        if "stop music" in text_lower or "stop the music" in text_lower or "pause music" in text_lower:
            success, message = self.youtube_player.stop()
            if success:
                self.tts.speak("Music stopped.")
            else:
                self.tts.speak("No music is playing.")
            return True

        # Weather commands
        if "weather" in text_lower or "mausam" in text_lower:
            weather_info = self.weather_time.get_weather()
            self.tts.speak(weather_info)
            return True

        # Time commands
        if ("time" in text_lower and "what" in text_lower) or "waqt kya hua" in text_lower:
            current_time = self.weather_time.get_current_time()
            self.tts.speak(f"The time is {current_time}")
            return True

        # Date commands
        if ("date" in text_lower and ("what" in text_lower or "today" in text_lower)) or "tareekh" in text_lower:
            current_date = self.weather_time.get_current_date()
            self.tts.speak(f"Today is {current_date}")
            return True

        # Day commands
        if "what day" in text_lower or "which day" in text_lower or "aaj kya din" in text_lower:
            day = self.weather_time.get_day_of_week()
            self.tts.speak(f"Today is {day}")
            return True

        # Alarm commands
        if "set alarm" in text_lower or "alarm lagao" in text_lower or ("set" in text_lower and "alarm" in text_lower):
            # Extract time from command (simple parsing)
            import re
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

                message = self.alarm_module.add_alarm(alarm_time, "Alarm")
                self.tts.speak(message)
            else:
                self.tts.speak("What time should I set the alarm for?")
            return True

        if "cancel alarm" in text_lower or "delete alarm" in text_lower:
            message = self.alarm_module.cancel_all_alarms()
            self.tts.speak(message)
            return True

        if ("show" in text_lower or "list" in text_lower or "my" in text_lower) and "alarm" in text_lower:
            message = self.alarm_module.get_alarms()
            self.tts.speak(message)
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

    def emergency_stop_music(self):
        """Emergency stop music without wake word (called from wake word detector)"""
        if self.youtube_player.is_playing_music():
            print("🚨 Emergency music stop triggered!")
            success, message = self.youtube_player.stop()
            return success
        return False

    def run(self):
        """Start the assistant"""
        try:
            print("\n" + "=" * 60)
            print(f"👂 {self.assistant_name} is now listening!")
            print(f"🎤 Say '{self.wake_word}' to activate")
            print(f"🎵 Say 'stop music' or just 'stop' to stop music (no wake word needed!)")
            print("🛑 Say 'goodbye' or 'exit' to stop the assistant")
            print("=" * 60 + "\n")

            # Start wake word detection with emergency stop callback
            self.wake_detector.start(self.on_wake_word_detected, self.emergency_stop_music)

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
