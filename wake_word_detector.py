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

        # Optimize for better wake word detection
        self.recognizer.energy_threshold = 300  # More sensitive
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.6  # Faster detection
        self.recognizer.phrase_threshold = 0.3

        # Adjust for ambient noise - faster calibration
        print("Calibrating for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibration complete!")

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
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

                try:
                    # Use Google's speech recognition
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"[Heard: {text}]")

                    # Check if any wake word is in the text
                    if any(wake_word in text for wake_word in self.wake_words):
                        print("✓ Wake word detected!")
                        if self.callback:
                            self.callback()

                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.RequestError as e:
                    print(f"Could not request results from speech recognition service; {e}")
                    time.sleep(1)

            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                pass
            except Exception as e:
                print(f"Error in wake word detection: {e}")
                time.sleep(1)

    def start(self, callback):
        """Start listening in a separate thread"""
        listener_thread = threading.Thread(target=self.listen_for_wake_word, args=(callback,))
        listener_thread.daemon = True
        listener_thread.start()
        return listener_thread

    def stop(self):
        """Stop listening for wake word"""
        self.is_listening = False
        print("Wake word detection stopped.")
