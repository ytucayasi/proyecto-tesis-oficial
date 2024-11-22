# import httpx
# import os
# from dotenv import load_dotenv
# import random

# # Cargar las variables de entorno desde el archivo .env
# load_dotenv()

# # Obtener la clave de API de Pexels desde las variables de entorno
# PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
# PEXELS_URL = 'https://api.pexels.com/v1/search'

# async def get_image_from_pexels(query: str) -> str:
#     try:
#         if not PEXELS_API_KEY:
#             raise ValueError("PEXELS_API_KEY no está configurada en las variables de entorno")

#         headers = {
#             'Authorization': PEXELS_API_KEY
#         }

#         # Mejorar la búsqueda añadiendo términos relevantes
#         enhanced_query = f"{query}"
#         print(f"Buscando imágenes para: {enhanced_query}")

#         params = {
#             'query': enhanced_query,
#             'per_page': 15,  # Solicitar más imágenes para tener más variedad
#             'orientation': 'landscape'  # Preferir imágenes horizontales para presentaciones
#         }

#         async with httpx.AsyncClient() as client:
#             response = await client.get(PEXELS_URL, headers=headers, params=params)

#         if response.status_code == 200:
#             data = response.json()
#             if data['photos']:
#                 # Seleccionar una imagen aleatoria de las primeras 15
#                 photo = random.choice(data['photos'])
#                 image_url = photo['src']['original']
#                 image_filename = f"{query.replace(' ', '_')}_{random.randint(1000, 9999)}.jpg"
#                 image_path = os.path.join('generated_resources', image_filename)

#                 # Descargar la imagen
#                 async with httpx.AsyncClient() as client:
#                     image_response = await client.get(image_url)
#                     with open(image_path, 'wb') as f:
#                         f.write(image_response.content)

#                 return image_path
#             else:
#                 raise Exception(f"No se encontraron imágenes para el query: {query}")
#         else:
#             raise Exception(f"Error fetching images: {response.status_code}")

#     except Exception as e:
#         raise Exception(f"Error during Pexels API call: {str(e)}")