"""
AI Brain Module
Integrates with ChatGPT (OpenAI) or Gemini (Google) to generate intelligent responses
"""
import os
from openai import OpenAI
import google.generativeai as genai


class AIBrain:
    def __init__(self, provider="openai", api_key=None):
        """
        Initialize AI Brain with specified provider

        Args:
            provider: 'openai' or 'gemini'
            api_key: API key for the chosen provider
        """
        self.provider = provider.lower()
        self.conversation_history = []

        # Response cache for instant replies to common questions
        self.response_cache = {
            'hello': "Hello! It's so nice to hear from you!",
            'hi': "Hi there! How can I help you today?",
            'how are you': "I'm doing wonderfully! Thanks for asking!",
            'what is your name': "I'm Hello Kitty, your friendly assistant!",
            'who are you': "I'm Hello Kitty, here to help you!",
            'thank you': "You're very welcome! Happy to help!",
            'thanks': "My pleasure! Anytime!",
        }

        if self.provider == "openai":
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-3.5-turbo"
            print(f"✓ AI Brain initialized with OpenAI (ChatGPT)")

        elif self.provider == "gemini":
            genai.configure(api_key=api_key)
            # Use gemini-2.5-flash which is fast and available
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.chat = self.model.start_chat(history=[])
            print(f"✓ AI Brain initialized with Google Gemini (gemini-2.5-flash)")

        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai' or 'gemini'")

        # System prompt to give the assistant personality
        self.system_prompt = """You are Hello Kitty, a friendly and helpful voice assistant.
Rules for responses:
- Keep responses SHORT (1-2 sentences maximum)
- Be cheerful, warm and friendly
- Speak naturally as if talking to a friend
- Avoid long explanations unless specifically asked
- Your responses will be spoken aloud, so keep them conversational and brief"""

    def get_response(self, user_input):
        """
        Get AI response for user input
        Uses cache for instant responses to common questions

        Args:
            user_input: User's question or statement

        Returns:
            str: AI generated response
        """
        # Check cache first for instant response
        user_lower = user_input.lower().strip()
        for key, response in self.response_cache.items():
            if key in user_lower:
                print("⚡ (cached response)")
                return response

        # If not in cache, use AI
        try:
            if self.provider == "openai":
                return self._get_openai_response(user_input)
            elif self.provider == "gemini":
                return self._get_gemini_response(user_input)
        except Exception as e:
            print(f"❌ Error getting AI response: {e}")
            return self._get_fallback_response(user_input)

    def _get_openai_response(self, user_input):
        """Get response from OpenAI ChatGPT"""
        # Build messages with conversation history
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history
        for entry in self.conversation_history[-10:]:  # Keep last 10 exchanges
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["assistant"]})

        # Add current user input
        messages.append({"role": "user", "content": user_input})

        # Get response from ChatGPT
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=60,  # Reduced for shorter, faster responses
            temperature=0.7
        )

        assistant_response = response.choices[0].message.content

        # Save to conversation history
        self.conversation_history.append({
            "user": user_input,
            "assistant": assistant_response
        })

        return assistant_response

    def _get_gemini_response(self, user_input):
        """Get response from Google Gemini with timeout and error handling"""
        try:
            # For first message, include system prompt
            if not self.conversation_history:
                full_input = f"{self.system_prompt}\n\nUser: {user_input}"
            else:
                full_input = user_input

            # Configure generation for faster, more concise responses
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'max_output_tokens': 100,  # Limit for faster responses
            }

            response = self.chat.send_message(
                full_input,
                generation_config=generation_config
            )
            assistant_response = response.text.strip()

            # Save to conversation history
            self.conversation_history.append({
                "user": user_input,
                "assistant": assistant_response
            })

            return assistant_response

        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
            # Return fallback response
            return self._get_fallback_response(user_input)

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        if self.provider == "gemini":
            self.chat = self.model.start_chat(history=[])
        print("Conversation history cleared.")

    def get_conversation_count(self):
        """Get number of exchanges in current conversation"""
        return len(self.conversation_history)

    def _get_fallback_response(self, user_input):
        """
        Get fallback response when AI fails
        Uses pattern matching for common questions
        """
        text = user_input.lower()

        # Common question patterns
        if any(word in text for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you today?"

        if 'how are you' in text:
            return "I'm doing great! Thanks for asking! How about you?"

        if 'your name' in text or 'who are you' in text:
            return "I'm Hello Kitty, your friendly AI assistant!"

        if 'time' in text and 'what' in text:
            import time
            return f"The current time is {time.strftime('%I:%M %p')}"

        if 'date' in text or 'day' in text:
            import time
            return f"Today is {time.strftime('%A, %B %d, %Y')}"

        if 'thank' in text:
            return "You're very welcome!"

        if any(word in text for word in ['joke', 'funny']):
            import random
            jokes = [
                "Why did the programmer quit? They didn't get arrays!",
                "What's a computer's favorite snack? Microchips!",
                "Why do programmers prefer dark mode? Because light attracts bugs!"
            ]
            return random.choice(jokes)

        if 'help' in text:
            return "I'm here to help! Just ask me anything, or say commands like 'play music' or 'tell me a joke'."

        # Default fallback
        return "I'm sorry, I'm having trouble right now. Can you please try asking that again?"
