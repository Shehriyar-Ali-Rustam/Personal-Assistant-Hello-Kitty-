"""
Speech Recognition Module
Converts user's speech to text
Optimized for better accuracy and speed
"""
import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Optimize recognizer settings for better accuracy and speed
        self.recognizer.energy_threshold = 300  # Lower = more sensitive to speech
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust to environment
        self.recognizer.pause_threshold = 0.8  # Wait longer for complete sentences (reduced from 0.8)
        self.recognizer.phrase_threshold = 0.3  # Start listening sooner
        self.recognizer.non_speaking_duration = 0.6  # Detect end of speech

        # Adjust for ambient noise - shorter calibration for faster startup
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

    def listen(self, timeout=10, phrase_time_limit=10):
        """
        Listen to user's speech and convert to text

        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for a phrase

        Returns:
            str: Recognized text or None if failed
        """
        print("\n🎤 Listening... (speak now)")

        try:
            with self.microphone as source:
                # Listen for user input
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            print("🔄 Processing your speech...")

            try:
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                print(f"📝 You said: {text}")
                return text

            except sr.UnknownValueError:
                print("❌ Sorry, I couldn't understand what you said.")
                return None
            except sr.RequestError as e:
                print(f"❌ Could not request results from speech recognition service; {e}")
                return None

        except sr.WaitTimeoutError:
            print("⏱️  No speech detected. Timeout.")
            return None
        except Exception as e:
            print(f"❌ Error during speech recognition: {e}")
            return None

    def listen_without_timeout(self):
        """Listen without timeout - waits indefinitely for speech"""
        print("\n🎤 Listening... (speak now)")

        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source)

            print("🔄 Processing your speech...")

            try:
                text = self.recognizer.recognize_google(audio)
                print(f"📝 You said: {text}")
                return text

            except sr.UnknownValueError:
                print("❌ Sorry, I couldn't understand what you said.")
                return None
            except sr.RequestError as e:
                print(f"❌ Could not request results; {e}")
                return None

        except Exception as e:
            print(f"❌ Error during speech recognition: {e}")
            return None
