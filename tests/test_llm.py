"""Tests for LLM providers."""

import pytest
from unittest.mock import Mock, patch
from farapraiser.llm.providers import OllamaProvider, LMStudioProvider


class TestOllamaProvider:
    """Test Ollama LLM provider."""
    
    @patch('farapraiser.llm.providers.requests.get')
    def test_is_available_success(self, mock_get):
        """Test availability check when Ollama is running."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        provider = OllamaProvider()
        assert provider.is_available() is True
    
    @patch('farapraiser.llm.providers.requests.get')
    def test_is_available_failure(self, mock_get):
        """Test availability check when Ollama is not running."""
        mock_get.side_effect = Exception("Connection refused")
        
        provider = OllamaProvider()
        assert provider.is_available() is False
    
    @patch('farapraiser.llm.providers.requests.post')
    def test_paraphrase_success(self, mock_post):
        """Test successful paraphrasing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": "This is a paraphrased version of the text."
        }
        mock_post.return_value = mock_response
        
        provider = OllamaProvider()
        variants = provider.paraphrase("Original text", tone="formal", num_variants=2)
        
        assert len(variants) == 2
        assert all(isinstance(v, str) for v in variants)
        assert mock_post.call_count == 2
    
    @patch('farapraiser.llm.providers.requests.post')
    def test_paraphrase_with_error(self, mock_post):
        """Test paraphrasing with API error."""
        mock_post.side_effect = Exception("API Error")
        
        provider = OllamaProvider()
        variants = provider.paraphrase("Original text", tone="formal", num_variants=2)
        
        assert len(variants) == 0


class TestLMStudioProvider:
    """Test LM Studio LLM provider."""
    
    @patch('farapraiser.llm.providers.requests.get')
    def test_is_available_success(self, mock_get):
        """Test availability check when LM Studio is running."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        provider = LMStudioProvider()
        assert provider.is_available() is True
    
    @patch('farapraiser.llm.providers.requests.get')
    def test_is_available_failure(self, mock_get):
        """Test availability check when LM Studio is not running."""
        mock_get.side_effect = Exception("Connection refused")
        
        provider = LMStudioProvider()
        assert provider.is_available() is False
    
    @patch('farapraiser.llm.providers.requests.post')
    def test_paraphrase_success(self, mock_post):
        """Test successful paraphrasing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "This is a paraphrased version."}}
            ]
        }
        mock_post.return_value = mock_response
        
        provider = LMStudioProvider()
        variants = provider.paraphrase("Original text", tone="academic", num_variants=1)
        
        assert len(variants) == 1
        assert variants[0] == "This is a paraphrased version."
    
    def test_build_prompt(self):
        """Test prompt building with different tones."""
        provider = OllamaProvider()
        
        prompt = provider._build_prompt("Test text", "formal")
        assert "formal" in prompt.lower()
        assert "Test text" in prompt
        
        prompt = provider._build_prompt("Test text", "academic")
        assert "academic" in prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
