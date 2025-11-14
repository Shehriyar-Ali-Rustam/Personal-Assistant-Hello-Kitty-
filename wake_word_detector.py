"""
Wake Word Detection Module
Listens for the wake word "Hello Kitty" to activate the assistant
"""
import speech_recognition as sr
import threading
import time


class WakeWordDetector:
    def __init__(self, wake_words=["hello kitty", "hey kitty"]):
        self.wake_words = [w.lower() for w in wake_words]
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.callback = None
        self.stop_music_callback = None  # Special callback for emergency stop

        # Optimize for better wake word detection
        self.recognizer.energy_threshold = 150  # Lower = more sensitive (improved from 300)
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Wait for complete phrase
        self.recognizer.phrase_threshold = 0.2  # Start listening sooner
        self.recognizer.non_speaking_duration = 0.5  # Quick detection

        # Adjust for ambient noise - better calibration
        print("🎙️  Calibrating wake word detector for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("✓ Wake word detector calibrated and ready!")

    def listen_for_wake_word(self, callback):
        """
        Continuously listen for the wake word
        Args:
            callback: Function to call when wake word is detected
        """
        self.callback = callback
        self.is_listening = True

        print(f"\nListening for wake words: {', '.join(self.wake_words)}...")
        print("Say one of the wake words to activate the assistant!\n")

        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen with a shorter timeout for better responsiveness
                    print("👂 Listening for wake word...", end="\r")
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)

                try:
                    # Use Google's speech recognition
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"🔊 [Heard: '{text}']                    ")

                    # EMERGENCY: Check for stop music command (works without wake word)
                    if self.stop_music_callback and ("stop music" in text or "stop the music" in text or "stop" in text):
                        print("🎵 Emergency stop music detected (no wake word needed)!")
                        if self.stop_music_callback():
                            print("✓ Music stopped successfully")
                            continue

                    # Check if any wake word is in the text
                    if any(wake_word in text for wake_word in self.wake_words):
                        print("✅ Wake word detected!")
                        if self.callback:
                            self.callback()
                    else:
                        print(f"   (Not a wake word, waiting...)")

                except sr.UnknownValueError:
                    # Speech was unintelligible
                    print("❓ Could not understand (background noise?)   ")
                except sr.RequestError as e:
                    print(f"❌ Could not request results from speech recognition service; {e}")
                    time.sleep(1)

            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                pass
            except Exception as e:
                print(f"⚠️  Error in wake word detection: {e}")
                time.sleep(1)

    def start(self, callback, stop_music_callback=None):
        """
        Start listening in a separate thread
        Args:
            callback: Function to call when wake word is detected
            stop_music_callback: Optional function to call for emergency music stop (no wake word needed)
        """
        self.stop_music_callback = stop_music_callback
        listener_thread = threading.Thread(target=self.listen_for_wake_word, args=(callback,))
        listener_thread.daemon = True
        listener_thread.start()
        return listener_thread

    def stop(self):
        """Stop listening for wake word"""
        self.is_listening = False
        print("Wake word detection stopped.")
