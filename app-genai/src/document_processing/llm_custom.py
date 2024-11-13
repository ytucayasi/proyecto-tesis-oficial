from langchain.llms.base import LLM
from typing import Optional, List, Any, Dict
import requests
from pydantic import Field, PrivateAttr
import json

class OpenRouterLLM(LLM):
    model_name: str = "meta-llama/llama-3.2-90b-vision-instruct:free"
    temperature: float = Field(default=0.7)
    
    _base_url: str = PrivateAttr()
    _api_key: str = PrivateAttr()
    _model: str = PrivateAttr()
    _referer: Optional[str] = PrivateAttr()
    _app_name: Optional[str] = PrivateAttr()

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        referer: Optional[str] = None,
        app_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__()
        self._base_url = base_url
        self._api_key = api_key
        self._model = model
        self.temperature = temperature
        self._referer = referer
        self._app_name = app_name

    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        
        if self._referer:
            headers["HTTP-Referer"] = self._referer
        if self._app_name:
            headers["X-Title"] = self._app_name

        try:
            data = {
                "model": self._model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that provides detailed academic summaries."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.temperature,
            }
            
            if stop:
                data["stop"] = stop

            print(f"Sending request to OpenRouter: {json.dumps(data, indent=2)}")  # Debug
            
            response = requests.post(
                f"{self._base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=120  # Aumentado el timeout
            )
            
            print(f"OpenRouter response status: {response.status_code}")  # Debug
            print(f"OpenRouter response: {response.text}")  # Debug
            
            if response.status_code != 200:
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                raise ValueError(f"Error from OpenRouter API: {error_detail} (Status: {response.status_code})")
            
            response_json = response.json()
            if 'choices' not in response_json or not response_json['choices']:
                raise ValueError("Invalid response format from OpenRouter")
            
            message_content = response_json['choices'][0]['message']['content']
            if not message_content:
                raise ValueError("Empty response from OpenRouter")
                
            return message_content
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error en la solicitud a OpenRouter: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar la respuesta de OpenRouter: {response.text}")
        except KeyError as e:
            raise ValueError(f"Respuesta inesperada de OpenRouter: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "model": self._model,
            "temperature": self.temperature,
            "base_url": self._base_url
        }

    def get_num_tokens(self, text: str) -> int:
        """Get the number of tokens present in the text."""
        # Implementación básica, podrías mejorarla con un tokenizer específico
        return len(text.split())