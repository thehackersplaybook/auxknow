"""
Tests for custom configuration functionality in AuxKnow.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from auxknow.engine.auxknow_config import AuxKnowConfig
from auxknow.engine.auxknow import AuxKnow
from auxknow.common.constants import Constants
from e2e.helpers.mock_llm_factory import MockLLMFactory


class TestCustomConfiguration(unittest.TestCase):
    """Test cases for custom configuration functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        os.rmdir(self.temp_dir)

    def test_default_config_loading(self):
        """Test loading default configuration when no file is provided."""
        config = AuxKnowConfig()
        
        # Should use default models
        self.assertEqual(config.get_model_for_task("standard"), "sonar")
        self.assertEqual(config.get_model_for_task("reasoning"), "sonar-reasoning")
        self.assertEqual(config.get_model_for_task("prompt_augmentation"), "gpt-4o-mini")
        self.assertEqual(len(config.custom_models), 0)

    def test_custom_models_validation(self):
        """Test validation of custom model configurations."""
        config = AuxKnowConfig()
        
        # Test valid custom models
        valid_models = {
            "standard": "sonar-pro",
            "reasoning": "sonar-reasoning-pro",
            "prompt_augmentation": "gpt-4o"
        }
        validated = config._validate_custom_models(valid_models, verbose=False)
        self.assertEqual(len(validated), 3)
        self.assertEqual(validated["standard"], "sonar-pro")

        # Test invalid task name
        invalid_task_models = {
            "invalid_task": "sonar",
            "standard": "sonar-pro"
        }
        validated = config._validate_custom_models(invalid_task_models, verbose=False)
        self.assertEqual(len(validated), 1)  # Only valid task should remain
        self.assertNotIn("invalid_task", validated)

        # Test invalid model name
        invalid_model_models = {
            "standard": "invalid-model",
            "reasoning": "sonar-reasoning"
        }
        validated = config._validate_custom_models(invalid_model_models, verbose=False)
        self.assertEqual(len(validated), 1)  # Only valid model should remain
        self.assertNotIn("standard", validated)

    def test_config_file_loading(self):
        """Test loading configuration from a JSON file."""
        # Create test config file
        test_config = {
            "custom_models": {
                "standard": "sonar-pro",
                "reasoning": "sonar-reasoning"
            },
            "auto_model_routing": False,
            "fast_mode": True
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)

        # Load configuration
        config = AuxKnowConfig.load_from_file(self.config_file, verbose=False)
        
        # Check custom models
        self.assertEqual(config.get_model_for_task("standard"), "sonar-pro")
        self.assertEqual(config.get_model_for_task("reasoning"), "sonar-reasoning")
        self.assertEqual(config.get_model_for_task("prompt_augmentation"), "gpt-4o-mini")  # Should use default
        
        # Check other settings
        self.assertFalse(config.auto_model_routing)
        self.assertTrue(config.fast_mode)

    def test_nonexistent_config_file(self):
        """Test handling of nonexistent configuration file."""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.json")
        config = AuxKnowConfig.load_from_file(nonexistent_file, verbose=False)
        
        # Should return default configuration
        self.assertEqual(config.get_model_for_task("standard"), "sonar")
        self.assertEqual(len(config.custom_models), 0)

    def test_invalid_json_config_file(self):
        """Test handling of invalid JSON in configuration file."""
        # Create invalid JSON file
        with open(self.config_file, 'w') as f:
            f.write("{ invalid json content")

        config = AuxKnowConfig.load_from_file(self.config_file, verbose=False)
        
        # Should return default configuration
        self.assertEqual(config.get_model_for_task("standard"), "sonar")
        self.assertEqual(len(config.custom_models), 0)

    def test_get_all_models(self):
        """Test getting all model mappings with custom overrides."""
        config = AuxKnowConfig()
        config.custom_models = {
            "standard": "sonar-pro",
            "reasoning": "sonar-reasoning"
        }
        
        all_models = config.get_all_models()
        
        # Should have all default tasks
        self.assertIn("standard", all_models)
        self.assertIn("reasoning", all_models)
        self.assertIn("deep_research", all_models)
        self.assertIn("prompt_augmentation", all_models)
        self.assertIn("fast_mode", all_models)
        
        # Custom models should override defaults
        self.assertEqual(all_models["standard"], "sonar-pro")
        self.assertEqual(all_models["reasoning"], "sonar-reasoning")
        self.assertEqual(all_models["deep_research"], "sonar-deep-research")  # Default

    @patch.dict(os.environ, {'PERPLEXITY_API_KEY': 'test_key', 'OPENAI_API_KEY': 'test_key'})
    def test_auxknow_with_config_file(self):
        """Test AuxKnow initialization with custom configuration file."""
        # Create test config file
        test_config = {
            "custom_models": {
                "standard": "sonar-pro",
                "fast_mode": "gpt-4o-mini"
            },
            "answer_length_in_paragraphs": 5,  # Use a setting that won't conflict with defaults
            "lines_per_paragraph": 10
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)

        # Initialize AuxKnow with config file (test mode to avoid API calls)
        auxknow = AuxKnow(
            config_file_path=self.config_file,
            test_mode=True,
            verbose=False,
            llm_factory=MockLLMFactory(),
            openai_api_key="test-key",
            perplexity_api_key="test-key"
        )
        
        # Check that custom models are loaded
        self.assertEqual(auxknow.config.get_model_for_task("standard"), "sonar-pro")
        self.assertEqual(auxknow.config.get_model_for_task("fast_mode"), "gpt-4o-mini")
        self.assertEqual(auxknow.config.get_model_for_task("reasoning"), "sonar-reasoning")  # Default
        
        # Check that config file settings are applied
        self.assertEqual(auxknow.config.answer_length_in_paragraphs, 5)
        self.assertEqual(auxknow.config.lines_per_paragraph, 10)

    @patch.dict(os.environ, {'PERPLEXITY_API_KEY': 'test_key', 'OPENAI_API_KEY': 'test_key'})
    def test_auxknow_parameter_override(self):
        """Test that explicit parameters override config file settings."""
        # Create test config file
        test_config = {
            "auto_model_routing": False,
            "fast_mode": False
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)

        # Initialize AuxKnow with config file but override some parameters
        auxknow = AuxKnow(
            config_file_path=self.config_file,
            auto_model_routing=True,  # Override config file setting
            fast_mode=True,          # Override config file setting
            test_mode=True,
            verbose=False,
            llm_factory=MockLLMFactory(),
            openai_api_key="test-key",
            perplexity_api_key="test-key"
        )
        
        # Explicit parameters should override config file
        self.assertTrue(auxknow.config.auto_model_routing)
        self.assertTrue(auxknow.config.fast_mode)


if __name__ == '__main__':
    unittest.main() 