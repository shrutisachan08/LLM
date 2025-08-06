import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="AIzaSyAU6prFaC2zvKxLliUEavoAKD3ylCmFPLM")

# List available models
models = genai.list_models()

# Print available model details
for model in models:
    print(f"Name: {model.name}")
    print(f"Base Model: {model.base_model_id if hasattr(model, 'base_model_id') else 'N/A'}")
    print(f"Supported Methods: {model.supported_generation_methods if hasattr(model, 'supported_generation_methods') else 'N/A'}")
    print("-" * 50)
