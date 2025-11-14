"""
Alarm Sound Module
Generates and plays alarm ringtone
"""
import pygame
import numpy as np
import time


class AlarmSound:
    def __init__(self):
        """Initialize alarm sound player"""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.is_playing = False
        print("✓ Alarm sound module initialized")

    def generate_beep_pattern(self):
        """
        Generate a pleasant alarm beep pattern
        Creates a series of tones similar to a classic alarm clock
        """
        sample_rate = 22050
        duration = 0.3  # Duration of each beep in seconds

        # Generate beep frequency (800 Hz - pleasant alarm tone)
        frequency = 800
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create beep sound wave
        wave = np.sin(2 * np.pi * frequency * t)

        # Add envelope for smoother sound (fade in/out)
        envelope = np.concatenate([
            np.linspace(0, 1, int(sample_rate * 0.05)),  # Fade in
            np.ones(int(sample_rate * (duration - 0.1))),  # Sustain
            np.linspace(1, 0, int(sample_rate * 0.05))   # Fade out
        ])

        wave = wave * envelope

        # Convert to 16-bit PCM
        wave = np.int16(wave * 32767)

        # Make stereo
        stereo_wave = np.column_stack((wave, wave))

        return pygame.sndarray.make_sound(stereo_wave)

    def play_alarm_ringtone(self, duration_seconds=10):
        """
        Play alarm ringtone for specified duration

        Args:
            duration_seconds: How long to play the alarm (default 10 seconds)
        """
        print("🔔 Playing alarm ringtone...")
        self.is_playing = True

        try:
            # Generate the beep sound
            beep = self.generate_beep_pattern()

            # Play pattern: beep-beep-pause-beep-beep-pause
            start_time = time.time()

            while (time.time() - start_time) < duration_seconds and self.is_playing:
                # Play two beeps
                beep.play()
                time.sleep(0.4)
                beep.play()
                time.sleep(0.4)

                # Short pause
                time.sleep(0.3)

                # Play two more beeps
                beep.play()
                time.sleep(0.4)
                beep.play()
                time.sleep(0.4)

                # Longer pause before repeating
                time.sleep(0.8)

        except Exception as e:
            print(f"⚠️  Error playing alarm sound: {e}")
        finally:
            self.is_playing = False
            pygame.mixer.stop()
            print("⏹️  Alarm ringtone stopped")

    def stop(self):
        """Stop the alarm ringtone"""
        self.is_playing = False
        pygame.mixer.stop()

    def play_quick_beep(self):
        """Play a quick single beep (for testing or short alerts)"""
        try:
            beep = self.generate_beep_pattern()
            beep.play()
            time.sleep(0.4)
        except Exception as e:
            print(f"⚠️  Error playing beep: {e}")
