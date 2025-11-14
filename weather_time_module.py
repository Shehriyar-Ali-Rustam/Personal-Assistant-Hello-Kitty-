"""
Weather and Time Module
Provides current time, date, and weather information
"""
import datetime
import requests
import pytz


class WeatherTimeModule:
    def __init__(self, city="Karachi", timezone="Asia/Karachi"):
        """
        Initialize Weather and Time module

        Args:
            city: Default city for weather
            timezone: Timezone for accurate time
        """
        self.city = city
        self.timezone = pytz.timezone(timezone)
        print(f"✓ Weather & Time module initialized (City: {city}, Timezone: {timezone})")

    def get_current_time(self):
        """Get current time in 12-hour format"""
        now = datetime.datetime.now(self.timezone)
        return now.strftime("%I:%M %p")

    def get_current_date(self):
        """Get current date in readable format"""
        now = datetime.datetime.now(self.timezone)
        return now.strftime("%A, %B %d, %Y")

    def get_day_of_week(self):
        """Get current day of the week"""
        now = datetime.datetime.now(self.timezone)
        return now.strftime("%A")

    def get_weather(self, city=None):
        """
        Get current weather information using wttr.in (no API key needed!)

        Args:
            city: City name (uses default if not provided)

        Returns:
            str: Weather description
        """
        if city is None:
            city = self.city

        try:
            # Use wttr.in - free weather service, no API key required
            url = f"http://wttr.in/{city}?format=%C+%t+%h+%w"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                weather_data = response.text.strip()
                # Parse the response: Condition Temperature Humidity Wind
                parts = weather_data.split()

                if len(parts) >= 2:
                    condition = parts[0]
                    temperature = parts[1]

                    return f"In {city}, it's {condition} with {temperature}"
                else:
                    return f"Current weather in {city}: {weather_data}"
            else:
                return f"Sorry, I couldn't get weather for {city}"

        except Exception as e:
            print(f"⚠️  Weather error: {e}")
            return "Sorry, I couldn't fetch the weather right now"

    def get_detailed_weather(self, city=None):
        """
        Get detailed weather with temperature, humidity, and wind

        Args:
            city: City name (uses default if not provided)

        Returns:
            dict: Detailed weather information
        """
        if city is None:
            city = self.city

        try:
            # Use wttr.in with JSON format
            url = f"http://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]

                return {
                    'temperature': current['temp_C'] + '°C',
                    'feels_like': current['FeelsLikeC'] + '°C',
                    'condition': current['weatherDesc'][0]['value'],
                    'humidity': current['humidity'] + '%',
                    'wind': current['windspeedKmph'] + ' km/h'
                }
            else:
                return None

        except Exception as e:
            print(f"⚠️  Detailed weather error: {e}")
            return None
