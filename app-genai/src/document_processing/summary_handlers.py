from typing import List
from fastapi import HTTPException
from langchain.docstore.document import Document
from .prompt_handlers import generate_prompt_templates

# Selección de plantilla según el tipo de resumen
def select_template_for_summary(topic: str, combined_text: str, summary_type: str):
    map_template, combine_template = generate_prompt_templates(topic)
    if summary_type == 'map':
        return map_template.format(text=combined_text, topic=topic)
    elif summary_type == 'combine':
        return combine_template.format(text=combined_text, topic=topic)
    else:
        raise ValueError("Tipo de resumen no válido. Usa 'map' o 'combine'.")

# Función principal para generar el resumen
async def generate_summary(
    relevant_chunks: List[Document],
    topic: str,
    llm,
    summary_type: str = 'map'  # Especifica el tipo de resumen ('map' o 'combine')
) -> str:
    try:
        # Combina el texto de los documentos relevantes
        combined_text = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
        
        # Selecciona la plantilla apropiada según el tipo de resumen
        prompt = select_template_for_summary(topic, combined_text, summary_type)
        
        # Genera el resumen con el LLM
        summary = llm(prompt)
        
        if not summary:
            raise HTTPException(
                status_code=500,
                detail="No se pudo generar un resumen"
            )
            
        return summary
        
    except Exception as e:
        print(f"Error en generate_summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el resumen: {str(e)}"
        )