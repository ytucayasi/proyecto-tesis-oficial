from langchain.prompts import PromptTemplate

# Define las plantillas de prompt
def generate_prompt_templates(topic: str):
    map_template = """
    IMPORTANTE: DEBES USAR EXACTAMENTE ESTE FORMATO DE MARCADO:

    ## [Título]
    ### [Sección Principal]
    * [Punto importante]
    * [Punto de lista]
    ** [Texto importante] **

    Genera un informe sobre {topic} usando EXACTAMENTE esta estructura:

    ## {topic}

    ### Introducción
    *  Contexto General
    * **Importancia**: [descripción]
    * **Relevancia**: [descripción]

    ### Contenido Principal
    *  Conceptos Clave
    * **Concepto 1**: [descripción]
    * **Concepto 2**: [descripción]

    ### Aplicaciones
    * **Ejemplo 1**: [descripción]
    * **Ejemplo 2**: [descripción]

    ### Conclusión
    *  Resumen
    * **Punto clave 1**: [descripción]
    * **Punto clave 2**: [descripción]

    NO USES OTROS FORMATOS DE MARCADO. SIGUE EXACTAMENTE ESTA ESTRUCTURA.

    INFORMACIÓN A ANALIZAR:
    {text}
    """

    combine_template = """
    IMPORTANTE: MANTÉN EXACTAMENTE ESTE FORMATO:

    ## {topic}

    ### Introducción
    *  Visión General
    * **Contexto**: [resumen del contexto]
    * **Objetivo**: [resumen del objetivo]

    ### Contenido Principal
    *  Análisis
    * **Punto 1**: [desarrollo]
    * **Punto 2**: [desarrollo]

    *  Hallazgos
    * **Hallazgo 1**: [descripción]
    * **Hallazgo 2**: [descripción]

    ### Conclusión
    *  Síntesis
    * **Conclusión 1**: [resumen]
    * **Conclusión 2**: [resumen]

    NO MODIFIQUES EL FORMATO. USA EXACTAMENTE LOS MARCADORES INDICADOS.

    CONTENIDO A SINTETIZAR:
    {text}
    """

    return (
        PromptTemplate(template=map_template, input_variables=["text", "topic"]),
        PromptTemplate(template=combine_template, input_variables=["text", "topic"])
    )

def generate_topic_query(topic: str) -> str:
    return f"""
    Encuentra información relevante sobre '{topic}', incluyendo:
    - Definiciones y conceptos principales
    - Características y aspectos clave
    - Ejemplos y casos de uso
    - Detalles técnicos importantes
    - Mejores prácticas y recomendaciones
    """