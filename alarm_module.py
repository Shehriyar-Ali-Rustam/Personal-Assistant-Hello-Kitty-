"""
Alarm Module
Manages alarms and reminders
"""
import datetime
import threading
import time
import json
import os
from pathlib import Path
from alarm_sound import AlarmSound


class AlarmModule:
    def __init__(self, alarm_callback=None):
        """
        Initialize Alarm module

        Args:
            alarm_callback: Function to call when alarm goes off
        """
        self.alarms = []
        self.alarm_callback = alarm_callback
        self.alarm_file = Path("alarms.json")
        self.running = True

        # Initialize alarm sound
        self.alarm_sound = AlarmSound()

        # Load existing alarms
        self.load_alarms()

        # Start alarm checker thread
        self.checker_thread = threading.Thread(target=self._check_alarms, daemon=True)
        self.checker_thread.start()

        print("✓ Alarm module initialized")

    def add_alarm(self, alarm_time, label="Alarm"):
        """
        Add a new alarm

        Args:
            alarm_time: datetime object or time string (HH:MM format)
            label: Description of the alarm

        Returns:
            str: Confirmation message
        """
        try:
            # Parse time if it's a string
            if isinstance(alarm_time, str):
                now = datetime.datetime.now()
                time_parts = alarm_time.split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1]) if len(time_parts) > 1 else 0

                alarm_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # If time has passed today, set for tomorrow
                if alarm_datetime <= now:
                    alarm_datetime += datetime.timedelta(days=1)
            else:
                alarm_datetime = alarm_time

            # Create alarm entry
            alarm = {
                'time': alarm_datetime.isoformat(),
                'label': label,
                'active': True
            }

            self.alarms.append(alarm)
            self.save_alarms()

            time_str = alarm_datetime.strftime("%I:%M %p")
            print(f"⏰ Alarm set for {time_str} - {label}")
            return f"Alarm set for {time_str}"

        except Exception as e:
            print(f"❌ Error setting alarm: {e}")
            return "Sorry, couldn't set the alarm"

    def get_alarms(self):
        """Get list of active alarms"""
        active_alarms = [a for a in self.alarms if a['active']]

        if not active_alarms:
            return "You have no active alarms"

        alarm_list = []
        for alarm in active_alarms:
            alarm_time = datetime.datetime.fromisoformat(alarm['time'])
            time_str = alarm_time.strftime("%I:%M %p on %A")
            alarm_list.append(f"{alarm['label']} at {time_str}")

        return "Your alarms: " + ", ".join(alarm_list)

    def cancel_all_alarms(self):
        """Cancel all alarms"""
        self.alarms = []
        self.save_alarms()
        print("🔕 All alarms cancelled")
        return "All alarms cancelled"

    def _check_alarms(self):
        """Background thread to check for alarm triggers"""
        while self.running:
            try:
                now = datetime.datetime.now()

                for alarm in self.alarms[:]:  # Copy list to avoid modification during iteration
                    if not alarm['active']:
                        continue

                    alarm_time = datetime.datetime.fromisoformat(alarm['time'])

                    # Check if alarm time has arrived (within 30 seconds window)
                    time_diff = (alarm_time - now).total_seconds()

                    if 0 <= time_diff <= 30:
                        # Trigger alarm
                        print(f"\n🔔 ALARM! {alarm['label']}")

                        # Play alarm ringtone in a separate thread (so it doesn't block)
                        ringtone_thread = threading.Thread(
                            target=self.alarm_sound.play_alarm_ringtone,
                            args=(10,),  # Play for 10 seconds
                            daemon=True
                        )
                        ringtone_thread.start()

                        # Call the callback (for voice notification)
                        if self.alarm_callback:
                            self.alarm_callback(alarm['label'])

                        # Mark as inactive and remove
                        alarm['active'] = False
                        self.alarms.remove(alarm)
                        self.save_alarms()

                # Check every 10 seconds
                time.sleep(10)

            except Exception as e:
                print(f"⚠️  Alarm checker error: {e}")
                time.sleep(10)

    def save_alarms(self):
        """Save alarms to file"""
        try:
            with open(self.alarm_file, 'w') as f:
                json.dump(self.alarms, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving alarms: {e}")

    def load_alarms(self):
        """Load alarms from file"""
        try:
            if self.alarm_file.exists():
                with open(self.alarm_file, 'r') as f:
                    self.alarms = json.load(f)
                print(f"📂 Loaded {len(self.alarms)} saved alarms")
        except Exception as e:
            print(f"⚠️  Error loading alarms: {e}")
            self.alarms = []

    def stop(self):
        """Stop the alarm checker thread"""
        self.running = False
