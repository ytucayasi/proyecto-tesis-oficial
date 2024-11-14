from typing import Dict, List
from langchain.docstore.document import Document
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os

async def process_pdf(file) -> List[Document]:
    try:
        content = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        loader = PDFPlumberLoader(temp_file_path)
        pages = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(pages)
        return chunks
    
    finally:
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)

def identify_sections(texts) -> Dict[str, list]:
    sections = {"Contenido Principal": []}
    current_section = "Contenido Principal"
    
    for doc in texts:
        content = doc.page_content.strip()
        first_line = content.split('\n')[0].strip()
        
        is_heading = any([
            first_line.isupper(),
            first_line.startswith('#'),
            len(first_line) < 50 and first_line.endswith(':'),
            first_line.endswith('¶'),
            first_line.startswith('Capítulo'),
            first_line.startswith('Sección'),
            all(word[0].isupper() for word in first_line.split() if word)
        ])
        
        if is_heading:
            current_section = first_line
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections[current_section].append(doc)
    
    return {k: v for k, v in sections.items() if v}