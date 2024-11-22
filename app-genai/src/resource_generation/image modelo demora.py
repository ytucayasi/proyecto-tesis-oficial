# import torch
# from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
# import os
# from typing import Optional
# from datetime import datetime
# import asyncio
# from functools import partial
# import numpy as np
# from PIL import Image
# import gc

# class ImageGenerator:
#     def __init__(self):
#         self.model_id = "stabilityai/stable-diffusion-2-1"
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.pipe = None
#         self.GENERATED_DIR = "generated_resources"
#         os.makedirs(self.GENERATED_DIR, exist_ok=True)

#     async def load_model(self):
#         """Carga el modelo de manera asíncrona"""
#         if self.pipe is None:
#             # Función para cargar el modelo
#             def load_pipeline():
#                 pipe = StableDiffusionPipeline.from_pretrained(
#                     self.model_id,
#                     torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
#                     safety_checker=None  # Desactivar safety checker para mejor rendimiento
#                 )
                
#                 # Usar DPMSolverMultistepScheduler para generación más rápida
#                 pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
                
#                 if self.device == "cuda":
#                     pipe.to(self.device)
#                     # Habilitar memory efficient attention
#                     pipe.enable_attention_slicing()
#                 return pipe

#             # Cargar el modelo de manera asíncrona
#             self.pipe = await asyncio.get_event_loop().run_in_executor(None, load_pipeline)

#     def _generate_prompt(self, titulo: str) -> str:
#         """Genera un prompt optimizado para la generación de imágenes"""
#         # Diccionario de prompts específicos para temas comunes
#         prompt_templates = {
#             "nacimiento de jesus": "detailed illustration of nativity scene, baby Jesus in manger, Mary and Joseph, shepherds and wise men, bethlehem stable, holy night, divine light, artistic style",
#             "caperucita roja": "storybook illustration of Little Red Riding Hood in forest, red cape, basket, enchanted woods, fairy tale style, detailed artwork",
#             "tres cerditos": "fairy tale illustration of Three Little Pigs, three houses (straw, wood, brick), wolf, whimsical style, detailed storybook art",
#             # Puedes agregar más templates según necesites
#         }
        
#         # Buscar un template específico o usar un formato general
#         base_prompt = prompt_templates.get(
#             titulo.lower(),
#             f"high quality illustration of {titulo}, detailed artwork, professional, educational style"
#         )
        
#         # Añadir modificadores para mejorar la calidad
#         enhanced_prompt = f"{base_prompt}, high resolution, detailed, professional quality, educational style"
#         return enhanced_prompt

#     async def generate_image(self, titulo: str) -> Optional[str]:
#         """Genera una imagen basada en el título dado"""
#         try:
#             # Cargar modelo si no está cargado
#             await self.load_model()
            
#             # Generar prompt optimizado
#             prompt = self._generate_prompt(titulo)
#             print(f"Generando imagen con prompt: {prompt}")

#             # Función para generar la imagen
#             def generate():
#                 with torch.inference_mode():
#                     image = self.pipe(
#                         prompt,
#                         num_inference_steps=30,
#                         guidance_scale=7.5,
#                         height=512,
#                         width=768  # Formato más apropiado para presentaciones
#                     ).images[0]
#                 return image

#             # Generar imagen de manera asíncrona
#             image = await asyncio.get_event_loop().run_in_executor(None, generate)

#             # Guardar la imagen
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"{titulo.replace(' ', '_')}_{timestamp}.png"
#             filepath = os.path.join(self.GENERATED_DIR, filename)
            
#             # Optimizar y guardar la imagen
#             image = self._optimize_image(image)
#             image.save(filepath, "PNG", optimize=True)

#             # Limpiar memoria GPU si está disponible
#             if self.device == "cuda":
#                 torch.cuda.empty_cache()
#                 gc.collect()

#             return filepath

#         except Exception as e:
#             print(f"Error generando imagen: {str(e)}")
#             return None

#     def _optimize_image(self, image: Image.Image) -> Image.Image:
#         """Optimiza la imagen para uso en presentaciones"""
#         # Asegurar que la imagen tenga el formato correcto para presentaciones
#         target_width = 1024
#         target_height = int((target_width / image.width) * image.height)
        
#         # Redimensionar la imagen manteniendo la proporción
#         image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
#         # Optimizar la calidad y el tamaño
#         image = image.convert('RGB')
        
#         return image

#     def cleanup(self):
#         """Limpia los recursos del modelo"""
#         if self.pipe is not None:
#             del self.pipe
#             self.pipe = None
#             if self.device == "cuda":
#                 torch.cuda.empty_cache()
#                 gc.collect()

# # Instancia global del generador
# generator = ImageGenerator()

# # Función principal para usar en resource_generation_service.py
# async def get_image_for_presentation(titulo: str) -> Optional[str]:
#     """Función principal para generar imágenes para presentaciones"""
#     try:
#         return await generator.generate_image(titulo)
#     except Exception as e:
#         print(f"Error en la generación de imagen: {str(e)}")
#         return None