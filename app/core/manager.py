# app/core/manager.py


class ModelManager:
    def __init__(self):
        self._providers = {}

    def register_provider(self, name, provider):
        self._providers[name] = provider

    def get_provider(self, name):
        if name not in self._providers:
            raise ValueError(f"Provider {name} not found")
        return self._providers[name]

    def list_providers(self):
        return list(self._providers.keys())


model_manager = ModelManager()  # Singleton instance
