"""
Alarm Sound Module
Generates and plays alarm ringtone using simple system beep
"""
import subprocess
import time
import threading


class AlarmSound:
    def __init__(self):
        """Initialize alarm sound player"""
        self.is_playing = False
        self.enabled = True
        print("✓ Alarm sound module initialized (using system beep)")

    def play_single_beep(self):
        """
        Play a single system beep using paplay (PulseAudio)
        """
        try:
            # Try using paplay with speaker-test to generate a tone
            # speaker-test generates test tones, we pipe it to paplay
            subprocess.run(
                ['timeout', '0.3', 'speaker-test', '-t', 'sine', '-f', '800', '-l', '1'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1
            )
        except Exception:
            # Fallback: try system beep command
            try:
                subprocess.run(['beep', '-f', '800', '-l', '300'],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             timeout=1)
            except Exception:
                # Final fallback: use simple printf bell character
                try:
                    subprocess.run(['bash', '-c', 'printf "\\a"'],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 timeout=1)
                except Exception:
                    pass  # Silent failure

    def play_alarm_ringtone(self, duration_seconds=10):
        """
        Play alarm ringtone for specified duration

        Args:
            duration_seconds: How long to play the alarm (default 10 seconds)
        """
        if not self.enabled:
            print("⚠️  Alarm ringtone disabled (audio system unavailable)")
            return

        print("🔔 Playing alarm ringtone...")
        self.is_playing = True

        try:
            # Play pattern: beep-beep-pause-beep-beep-pause
            start_time = time.time()

            while (time.time() - start_time) < duration_seconds and self.is_playing:
                # Play two beeps
                self.play_single_beep()
                time.sleep(0.4)  # Wait for beep to finish

                self.play_single_beep()
                time.sleep(0.4)

                # Short pause
                time.sleep(0.3)

                # Play two more beeps
                self.play_single_beep()
                time.sleep(0.4)

                self.play_single_beep()
                time.sleep(0.4)

                # Longer pause before repeating
                time.sleep(0.8)

        except Exception as e:
            print(f"⚠️  Error playing alarm sound: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_playing = False
            print("⏹️  Alarm ringtone stopped")

    def stop(self):
        """Stop the alarm ringtone"""
        self.is_playing = False

    def play_quick_beep(self):
        """Play a quick single beep (for testing or short alerts)"""
        try:
            self.play_single_beep()
            time.sleep(0.4)
        except Exception as e:
            print(f"⚠️  Error playing beep: {e}")
