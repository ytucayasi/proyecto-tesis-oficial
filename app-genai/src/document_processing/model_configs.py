import os

MODEL_CONFIGS = {
    "openai": {
        "requires_api_key": True,
        "api_key_env": "OPENAI_API_KEY",
        "base_url": None,
        "model_name": None
    },
    "llava-llama3": {
        "requires_api_key": False,
        "api_key_env": None,
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "model_name": "llava-llama3:latest"
    },
    "llama-90b": {
        "requires_api_key": True,
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "model_name": "meta-llama/llama-3.2-90b-vision-instruct:free",
        "is_openrouter": True,
        "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
        "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
    },
    "zephyr-7b": {
        "requires_api_key": True,
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "model_name": "huggingfaceh4/zephyr-7b-beta:free",
        "is_openrouter": True,
        "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
        "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
    },
    "gemma-9b": {
        "requires_api_key": True,
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "model_name": "google/gemma-2-9b-it:free",
        "is_openrouter": True,
        "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
        "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
    },
    "llama-3b": {
        "requires_api_key": True,
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "model_name": "meta-llama/llama-3.2-3b-instruct:free",
        "is_openrouter": True,
        "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
        "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
    },
    "llama-70b": {
        "requires_api_key": True,
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "model_name": "meta-llama/llama-3.1-70b-instruct:free",
        "is_openrouter": True,
        "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
        "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
    }
}