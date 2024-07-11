import json
import pandas as pd
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

# Função para ler o arquivo JSON linha por linha
def read_json_lines(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def adjust_date_format(date_str):
    # Remover o prefixo "D:" e ajustar para formato ISO 8601
    date_str = date_str[2:]
    # Remover o apóstrofo no offset do fuso horário
    if "'" in date_str:
        date_str = date_str.replace("'", "")
    return date_str

# Carregar o arquivo JSON linha por linha
file_path = 'pdf_metadata_with_features.json'
data = read_json_lines(file_path)


for entry in data:
    entry['publication_date'] = adjust_date_format(entry['publication_date'])

# Converter para um DataFrame do Pandas
df = pd.DataFrame(data)

# Converter as datas de publicação para um formato de data do Pandas
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%Y%m%d%H%M%S%z', utc=True)

# Definir uma ontologia simples
ontology = {
    'Cultural Heritage': ['heritage', 'cultural', 'museum', 'artifact'],
    'Digital Technology': ['digital', 'virtual', '3D', 'augmented reality', 'VR', 'AR'],
    'Restoration': ['restoration', 'conservation', 'preservation'],
    'Education': ['teaching', 'education', 'learning']
}

# Função para categorizar palavras-chave com base na ontologia
def categorize_keywords(keywords, ontology):
    categories = []
    for keyword in keywords.split(','):
        keyword = keyword.strip().lower()
        for category, terms in ontology.items():
            if any(term in keyword for term in terms):
                categories.append(category)
                break
    return categories

# Aplicar a função de categorização
df['categories'] = df['keywords'].apply(lambda x: categorize_keywords(x, ontology))

# Exibir as primeiras linhas do DataFrame com as categorias
print(df[['title', 'keywords', 'categories']].head())




# Criação do grafo RDF
g = Graph()
EX = Namespace('http://example.org/')

# Adicionar classes de ontologia (categorias)
for category in ontology.keys():
    class_uri = URIRef(EX[category.replace(' ', '_')])
    g.add((class_uri, RDF.type, OWL.Class))
    g.add((class_uri, RDFS.label, Literal(category)))

# Adicionar palavras-chave como subclasses ou indivíduos
for category, keywords in ontology.items():
    category_uri = URIRef(EX[category.replace(' ', '_')])
    for keyword in keywords:
        keyword_uri = URIRef(EX[keyword.replace(' ', '_')])
        g.add((keyword_uri, RDF.type, OWL.Class))
        g.add((keyword_uri, RDFS.label, Literal(keyword)))
        g.add((keyword_uri, RDFS.subClassOf, category_uri))

# Serializar grafo para formato RDF/XML
output_path = 'ontology.owl'
g.serialize(destination=output_path, format='xml')

print(f'Ontologia salva em {output_path}')







# Explodir as categorias para facilitar a contagem
df_exploded = df.explode('categories')

# Contar a frequência das categorias por ano
category_counts = df_exploded.groupby([df_exploded['publication_date'].dt.year, 'categories']).size().unstack(fill_value=0)

# Exibir a contagem de categorias por ano
print(category_counts)

# Plotar a frequência das categorias ao longo do tempo
# category_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
# plt.xlabel('Ano')
# plt.ylabel('Frequência')
# plt.title('Frequência das Categorias ao Longo do Tempo')
# plt.legend(title='Categorias')
# plt.show()

