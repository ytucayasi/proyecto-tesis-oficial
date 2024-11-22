import os
import httpx
from typing import Optional
from datetime import datetime
import asyncio
from deep_translator import GoogleTranslator
import time
import json
import random  # Añadimos esta importación

class ImageGenerator:
    def __init__(self):
        self.GENERATED_DIR = "generated_resources"
        self.translator = GoogleTranslator(source='auto', target='en')
        self.API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
        self.headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
        os.makedirs(self.GENERATED_DIR, exist_ok=True)

    async def translate_to_english(self, text: str) -> str:
        try:
            def translate():
                return self.translator.translate(text)
            return await asyncio.get_event_loop().run_in_executor(None, translate)
        except Exception as e:
            print(f"Error en traducción: {str(e)}")
            return text

    def _enhance_prompt(self, title: str, variation: str = "") -> str:
        """Mejora el prompt para generar imágenes más realistas y detalladas con variaciones"""
        if variation:
            # Si es una sección específica, adaptamos el prompt
            base_prompt = f"{title} - {variation}"
        else:
            base_prompt = title
            
        # Añadir variedad en el estilo y la composición
        style_variations = [
            "photographic style, realistic, detailed, 8k quality",
            "cinematic composition, dramatic lighting, high detail",
            "professional photograph, artistic composition, vibrant",
            "documentary style, natural lighting, detailed view",
            "artistic interpretation, professional quality, detailed render"
        ]
        
        # Seleccionar una variación de estilo aleatoria
        selected_style = random.choice(style_variations)
        
        return f"{base_prompt}, {selected_style}"

    async def query_with_retry(self, payload: dict, max_retries: int = 5) -> bytes:
        """Consulta la API con reintentos y manejo de cola"""
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        self.API_URL,
                        headers=self.headers,
                        json=payload
                    )

                    # Si el modelo está cargando o en cola
                    if response.status_code == 503:
                        response_json = response.json()
                        if "estimated_time" in response_json:
                            wait_time = response_json["estimated_time"]
                            print(f"Modelo en cola, esperando {wait_time} segundos...")
                            await asyncio.sleep(wait_time)
                            continue
                
                    # Si la respuesta es exitosa
                    if response.status_code == 200:
                        return response.content

                    # Otros errores
                    response.raise_for_status()

            except (httpx.ReadTimeout, httpx.ReadError) as e:
                wait_time = 2 ** attempt  # Espera exponencial
                print(f"Timeout en intento {attempt + 1}, esperando {wait_time} segundos...")
                if attempt < max_retries - 1:
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"Tiempo de espera agotado después de {max_retries} intentos") from e

            except Exception as e:
                print(f"Error en intento {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise

        raise Exception("Máximo número de intentos alcanzado")

    async def generate_image(self, titulo: str) -> Optional[str]:
        """Genera una imagen usando la API de Hugging Face"""
        try:
            english_title = await self.translate_to_english(titulo)
            print(f"Título traducido: {english_title}")

            # Si el título contiene un guion, es una sección específica
            if " - " in titulo:
                base_title, section = titulo.split(" - ", 1)
                prompt = self._enhance_prompt(english_title, variation="")
            else:
                prompt = self._enhance_prompt(english_title)

            print(f"Generando imagen con prompt: {prompt}")

            payload = {
                "inputs": prompt
            }

            print("Iniciando generación de imagen...")
            image_data = await self.query_with_retry(payload)
            print("Imagen generada exitosamente")

            # Guardar la imagen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{titulo.replace(' ', '_')}_{timestamp}.png"
            filepath = os.path.join(self.GENERATED_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(image_data)

            print(f"Imagen guardada en: {filepath}")
            return filepath

        except Exception as e:
            print(f"Error generando imagen: {str(e)}")
            import traceback
            print(f"Traceback completo: {traceback.format_exc()}")
            return None

# Instancia global del generador
generator = ImageGenerator()

async def get_image_for_presentation(titulo: str) -> Optional[str]:
    """Función principal para generar imágenes para presentaciones"""
    try:
        return await generator.generate_image(titulo)
    except Exception as e:
        print(f"Error en la generación de imagen: {str(e)}")
        return None