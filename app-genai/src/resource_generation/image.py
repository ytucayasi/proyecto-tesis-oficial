import httpx
import os
from dotenv import load_dotenv
from pptx import Presentation
from pptx.util import Inches
from datetime import datetime

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API de Pexels desde las variables de entorno
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')  # Cargamos la clave de la API desde el entorno
PEXELS_URL = 'https://api.pexels.com/v1/search'

# Función para obtener una imagen de Pexels
async def get_image_from_pexels(query: str) -> str:
    try:
        # Verificar si la clave de API está disponible
        if not PEXELS_API_KEY:
            raise ValueError("PEXELS_API_KEY no está configurada en las variables de entorno")

        headers = {
            'Authorization': PEXELS_API_KEY
        }

        # Asegúrate de que el query no tenga caracteres extraños
        query = query.strip()  # Eliminar posibles espacios extra al principio y al final
        print(f"Buscando imágenes para: {query}")  # Depuración para ver qué query se está enviando

        params = {
            'query': query,  # Usar el título del slide como query
            'per_page': 1  # Limitar a 1 imagen por búsqueda
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(PEXELS_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                # Obtén la URL de la imagen más relevante
                image_url = data['photos'][0]['src']['original']
                image_filename = os.path.basename(image_url)
                image_path = os.path.join('generated_resources', image_filename)

                # Descargar la imagen
                async with httpx.AsyncClient() as client:
                    image_response = await client.get(image_url)
                    with open(image_path, 'wb') as f:
                        f.write(image_response.content)

                return image_path
            else:
                raise Exception(f"No se encontraron imágenes para el query: {query}")
        else:
            raise Exception(f"Error fetching images: {response.status_code}")

    except Exception as e:
        raise Exception(f"Error during Pexels API call: {str(e)}")
