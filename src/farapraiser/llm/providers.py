"""LLM integration for paraphrasing."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
import json


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def paraphrase(self, text: str, tone: str = "formal", num_variants: int = 3) -> List[str]:
        """Generate paraphrased variants of the text."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        pass
    
    def _build_prompt(self, text: str, tone: str) -> str:
        """Build the paraphrasing prompt."""
        tone_instructions = {
            "formal": "Use formal, professional language.",
            "academic": "Use academic style with scholarly vocabulary.",
            "casual": "Use conversational, everyday language.",
            "technical": "Use precise technical terminology.",
            "simplified": "Use simple, clear language that's easy to understand.",
        }
        
        instruction = tone_instructions.get(tone, tone_instructions["formal"])
        
        return f"""Paraphrase the following text. {instruction}

Original text:
{text}

Paraphrased version (maintain the same meaning but use different words and structure):"""


class OllamaProvider(LLMProvider):
    """LLM provider using Ollama."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2", timeout: int = 60):
        """Initialize Ollama provider."""
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
    
    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def paraphrase(self, text: str, tone: str = "formal", num_variants: int = 3) -> List[str]:
        """Generate paraphrased variants using Ollama."""
        variants = []
        
        for i in range(num_variants):
            prompt = self._build_prompt(text, tone)
            if i > 0:
                prompt += f"\n\n(Generate a different variation from previous attempts)"
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7 + (i * 0.1),  # Vary temperature for diversity
                            "top_p": 0.9,
                        }
                    },
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    paraphrased = result.get("response", "").strip()
                    if paraphrased:
                        variants.append(paraphrased)
                        
            except Exception as e:
                print(f"Error generating variant {i+1}: {e}")
                continue
        
        return variants


class LMStudioProvider(LLMProvider):
    """LLM provider using LM Studio."""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", model: str = "local-model", timeout: int = 60):
        """Initialize LM Studio provider."""
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
    
    def is_available(self) -> bool:
        """Check if LM Studio is running."""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def paraphrase(self, text: str, tone: str = "formal", num_variants: int = 3) -> List[str]:
        """Generate paraphrased variants using LM Studio."""
        variants = []
        
        for i in range(num_variants):
            prompt = self._build_prompt(text, tone)
            if i > 0:
                prompt += f"\n\n(Generate a different variation from previous attempts)"
            
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant that paraphrases text while maintaining its meaning."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7 + (i * 0.1),
                        "max_tokens": 1024,
                    },
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    choices = result.get("choices", [])
                    if choices:
                        paraphrased = choices[0].get("message", {}).get("content", "").strip()
                        if paraphrased:
                            variants.append(paraphrased)
                            
            except Exception as e:
                print(f"Error generating variant {i+1}: {e}")
                continue
        
        return variants
