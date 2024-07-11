import os
import json
import fitz
import re

# Diretório onde os PDFs estão armazenados
pdf_directory = 'C:/Users/Professor/Documents/Corpo_textual'

metadata = []

# Função para extrair o texto de um PDF
def extract_text_from_first_page(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(min(5, len(doc))):  # Garantir que não excedemos o número de páginas do documento
        text += doc[page_num].get_text()
    doc.close()
    return text

# Função para encontrar o país de publicação no texto do PDF
def find_country(text):
    country_patterns = [
        r'\bUSA\b', r'\bUnited States\b', r'\bCanada\b',
        r'\bUK\b', r'\bUnited Kingdom\b', r'\bAustralia\b', r'\bBrazil\b',r'\bChina\b', r'\bJapan\b', r'\bSpain\b', r'\bKorea\b',r'\bBelgium\b',r'\bItaly\b',r'\bThailand\b',r'\bIndia\b'
    ]
    for pattern in country_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group()
    return None

# Função para encontrar o link de publicação no texto do PDF
def find_publication_link(text):
    url_pattern = r'https?://(?!creativecommons)[^\s]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group()
    return None

# Função para encontrar palavras-chave no texto do PDF
def find_keywords(text):
    keyword_patterns = [
        r'\bKeywords\b:?\s*(.*)',  
        r'\bPalavras-chave\b:?\s*(.*)', 
        r'\bPalabras clave\b:?\s*(.*)'  
    ]
    for pattern in keyword_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Retorna a primeira correspondência encontrada
            return match.group(1).strip()
    return None

# Percorre todos os arquivos no diretório
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        file_path = os.path.join(pdf_directory, filename)
        pdf_info = {
            'filename': filename,
            'title': None,  
            'author': None,  
            'publication_date': None,
            'country': None,
            'publication_link': None,
            'keywords': None 
        }
        doc = fitz.open(file_path)

        # Extrai metadados do PDF
        pdf_metadata = doc.metadata
        pdf_info['title'] = pdf_metadata.get('title')
        pdf_info['author'] = pdf_metadata.get('author')
        pdf_info['publication_date'] = pdf_metadata.get('creationDate')

         # Extrai texto das primeiras páginas
        first_page_text = extract_text_from_first_page(file_path)
        
        # Busca por país de publicação e link de publicação no texto
        pdf_info['country'] = find_country(first_page_text)
        pdf_info['publication_link'] = find_publication_link(first_page_text)
        pdf_info['keywords'] = find_keywords(first_page_text)
      
        doc.close()
        
        metadata.append(pdf_info)

# Salva os metadados em um arquivo JSON
with open('pdf_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)
