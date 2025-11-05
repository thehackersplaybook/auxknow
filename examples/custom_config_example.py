"""
Example: Using Custom Configuration with AuxKnow

This example demonstrates how to use a custom configuration file to override
default model selections and other settings in AuxKnow.
"""

import os
from auxknow.engine.auxknow import AuxKnow

def main():
    """Demonstrate using custom configuration with AuxKnow."""
    
    # Example 1: Using a custom configuration file
    print("=== Example 1: Using Custom Configuration File ===")
    
    # Create a custom config (you can also edit auxknow_config.json)
    custom_config = {
        "custom_models": {
            "standard": "sonar-pro",           # Override standard model
            "reasoning": "sonar-reasoning-pro", # Override reasoning model  
            "prompt_augmentation": "gpt-4o",   # Override prompt augmentation model
            "fast_mode": "sonar",              # Keep fast mode as sonar
            "deep_research": "sonar-deep-research"  # Keep deep research default
        },
        "auto_model_routing": True,
        "enable_reasoning": True,
        "performance_logging_enabled": True
    }
    
    # Save to a temporary config file
    import json
    config_path = "temp_config.json"
    with open(config_path, 'w') as f:
        json.dump(custom_config, f, indent=2)
    
    try:
        # Initialize AuxKnow with custom config
        auxknow = AuxKnow(
            config_file_path=config_path,
            verbose=True
        )
        
        # Ask a question - this will use your custom model configuration
        response = auxknow.ask("What are the benefits of renewable energy?")
        print(f"Answer: {response.answer[:200]}...")
        print(f"Citations: {len(response.citations)} found")
        
        # Show current configuration
        print("\n=== Current Model Configuration ===")
        all_models = auxknow.config.get_all_models()
        for task, model in all_models.items():
            is_custom = task in auxknow.config.custom_models
            status = " (CUSTOM)" if is_custom else " (DEFAULT)"
            print(f"{task}: {model}{status}")
            
    finally:
        # Clean up temp file
        if os.path.exists(config_path):
            os.remove(config_path)
    
    print("\n=== Example 2: Programmatic Configuration ===")
    
    # You can also update configuration programmatically
    auxknow2 = AuxKnow(verbose=True)
    
    # Update configuration after initialization
    auxknow2.set_config({
        "custom_models": {
            "standard": "gpt-4o-mini",  # Use OpenAI model for standard tasks
            "reasoning": "o4-mini-deep-research"      # Use unbiased reasoning model
        },
        "auto_model_routing": False,
        "fast_mode": True
    })
    
    print("\n=== Updated Model Configuration ===")
    all_models = auxknow2.config.get_all_models()
    for task, model in all_models.items():
        is_custom = task in auxknow2.config.custom_models
        status = " (CUSTOM)" if is_custom else " (DEFAULT)"
        print(f"{task}: {model}{status}")

if __name__ == "__main__":
    main() 