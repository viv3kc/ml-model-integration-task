# app/core/config.py
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""

    def __init__(self):
        # API Keys
        self._openai_api_key = os.getenv("OPENAI_API_KEY")
        # Default settings
        self._default_model = os.getenv("DEFAULT_MODEL", "openai")
        # Validate settings on initialization
        self.validate()

    @property
    def openai_api_key(self):
        return self._openai_api_key

    @property
    def default_model(self):
        return self._default_model

    def validate(self):
        if not self._openai_api_key or self._openai_api_key.strip() == "":
            raise ValueError(
                "OPENAI_API_KEY environment variable is empty or not set. Please set it in your .env file."
            )
        if not self._default_model or self._default_model.strip() == "":
            raise ValueError(
                "DEFAULT_MODEL environment variable is empty. Please set it in your .env file."
            )


# Create a single instance
settings = Settings()
