"""LLM package."""

from farapraiser.llm.providers import LLMProvider, OllamaProvider, LMStudioProvider

__all__ = ["LLMProvider", "OllamaProvider", "LMStudioProvider"]


def get_provider(provider_type: str, **kwargs) -> LLMProvider:
    """Get LLM provider instance."""
    providers = {
        "ollama": OllamaProvider,
        "lmstudio": LMStudioProvider,
    }
    
    provider_class = providers.get(provider_type.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider_type}")
    
    return provider_class(**kwargs)
