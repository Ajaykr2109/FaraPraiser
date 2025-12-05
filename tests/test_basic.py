"""Unit tests for FaraPraiser."""

import pytest
from pathlib import Path
from farapraiser.parsers.base import DocumentBlock, BlockType
from farapraiser.utils.config import Config
from farapraiser.utils.hardware import HardwareDetector


class TestConfig:
    """Test configuration management."""
    
    def test_config_initialization(self):
        """Test that config initializes with defaults."""
        config = Config()
        assert config.config is not None
        assert "llm" in config.config
        assert "ui" in config.config
    
    def test_config_get(self):
        """Test getting config values."""
        config = Config()
        provider = config.get("llm.provider")
        assert provider in ["ollama", "lmstudio"]
    
    def test_config_set(self, tmp_path):
        """Test setting config values."""
        config = Config()
        # Use temp path for testing
        config.config_file = tmp_path / "test_config.json"
        config.set("test.key", "test_value")
        assert config.get("test.key") == "test_value"


class TestHardwareDetector:
    """Test hardware detection."""
    
    def test_get_system_info(self):
        """Test getting system information."""
        info = HardwareDetector.get_system_info()
        assert "platform" in info
        assert "ram_gb" in info
        assert "cpu_count" in info
        assert info["ram_gb"] > 0
    
    def test_recommend_model(self):
        """Test model recommendation."""
        model = HardwareDetector.recommend_model()
        assert isinstance(model, str)
        assert len(model) > 0
    
    def test_get_optimal_threads(self):
        """Test optimal thread calculation."""
        threads = HardwareDetector.get_optimal_threads()
        assert threads >= 1


class TestDocumentBlock:
    """Test document block."""
    
    def test_paragraph_block(self):
        """Test paragraph block text extraction."""
        block = DocumentBlock(
            block_type=BlockType.PARAGRAPH,
            content="This is a test paragraph.",
            metadata={},
            index=0
        )
        assert block.get_text() == "This is a test paragraph."
    
    def test_list_block(self):
        """Test list block text extraction."""
        block = DocumentBlock(
            block_type=BlockType.LIST,
            content=["Item 1", "Item 2", "Item 3"],
            metadata={},
            index=0
        )
        text = block.get_text()
        assert "• Item 1" in text
        assert "• Item 2" in text
        assert "• Item 3" in text
    
    def test_table_block(self):
        """Test table block text extraction."""
        block = DocumentBlock(
            block_type=BlockType.TABLE,
            content=[["A", "B"], ["C", "D"]],
            metadata={},
            index=0
        )
        text = block.get_text()
        assert "A | B" in text
        assert "C | D" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
