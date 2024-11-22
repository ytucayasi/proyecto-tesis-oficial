from fastapi import HTTPException
import os
from langchain_community.llms import OpenAI, Ollama
from .llm_custom import OpenRouterLLM
from .model_configs import MODEL_CONFIGS

def get_llm(process_request):
    model_config = MODEL_CONFIGS.get(process_request.model_type)
    if not model_config:
        raise HTTPException(
            status_code=400,
            detail=f"Modelo no soportado: {process_request.model_type}"
        )

    if model_config["requires_api_key"]:
        api_key = os.getenv(model_config["api_key_env"])
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail=f"API key no encontrada para {process_request.model_type}"
            )

    try:
        if process_request.model_type == "openai":
            return OpenAI(temperature=process_request.temperature)
        elif process_request.model_type == "llama-90b":
            return OpenRouterLLM(
                base_url=model_config["base_url"],
                api_key=os.getenv(model_config["api_key_env"]),
                model=model_config["model_name"],
                temperature=process_request.temperature,
                referer=model_config.get("referer"),
                app_name=model_config.get("app_name")
            )
        elif process_request.model_type == "zephyr-7b":
            return OpenRouterLLM(
                base_url=model_config["base_url"],
                api_key=os.getenv(model_config["api_key_env"]),
                model=model_config["model_name"],
                temperature=process_request.temperature,
                referer=model_config.get("referer"),
                app_name=model_config.get("app_name")
            )
        elif process_request.model_type == "gemma-9b":
            return OpenRouterLLM(
                base_url=model_config["base_url"],
                api_key=os.getenv(model_config["api_key_env"]),
                model=model_config["model_name"],
                temperature=process_request.temperature,
                referer=model_config.get("referer"),
                app_name=model_config.get("app_name")
            )
        elif process_request.model_type == "llama-3b":
            return OpenRouterLLM(
                base_url=model_config["base_url"],
                api_key=os.getenv(model_config["api_key_env"]),
                model=model_config["model_name"],
                temperature=process_request.temperature,
                referer=model_config.get("referer"),
                app_name=model_config.get("app_name")
            )
        elif process_request.model_type == "llama-70b":
            return OpenRouterLLM(
                base_url=model_config["base_url"],
                api_key=os.getenv(model_config["api_key_env"]),
                model=model_config["model_name"],
                temperature=process_request.temperature,
                referer=model_config.get("referer"),
                app_name=model_config.get("app_name")
            )
        else:
            return Ollama(
                model=model_config["model_name"],
                temperature=process_request.temperature,
                base_url=model_config["base_url"]
            )
    except Exception as e:
        print(f"Error al inicializar modelo: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error inicializando el modelo {process_request.model_type}: {str(e)}"
        )