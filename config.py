"""
Configuration module for Hello Kitty Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration settings for the assistant"""

    # AI Provider settings
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Assistant settings
    WAKE_WORD = os.getenv("WAKE_WORD", "hello kitty")
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Hello Kitty")

    # Voice settings
    VOICE_RATE = int(os.getenv("VOICE_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "0.9"))

    # Speech recognition settings
    SPEECH_TIMEOUT = int(os.getenv("SPEECH_TIMEOUT", "10"))
    PHRASE_TIME_LIMIT = int(os.getenv("PHRASE_TIME_LIMIT", "15"))

    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []

        if cls.AI_PROVIDER not in ["openai", "gemini"]:
            errors.append(f"Invalid AI_PROVIDER: {cls.AI_PROVIDER}. Must be 'openai' or 'gemini'")

        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when using OpenAI")

        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required when using Gemini")

        if errors:
            raise ValueError("\n".join(errors))

        return True
