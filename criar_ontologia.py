import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import defaultdict

# Carregar o JSON
with open('pdf_metadata_with_features.json', 'r', encoding='utf-8') as f:
    artigos = json.load(f)

# Extrair embeddings e informações adicionais
embeddings = []
ids = []
titles = []
keywords = []
autores = []

for artigo in artigos:
    embeddings.append(artigo['embeddings'])
    titles.append(artigo['filename'])
    ids.append(artigo['title'])
    keywords.append(artigo['keywords'])
    autores.append(artigo.get('author', ''))

# Converter embeddings para numpy array
embeddings = np.array(embeddings)

# Definir categorias e subcategorias
categorias = {
    "Tecnologia Digital": ["Digitalização", "Armazenamento", "Software", "Acesso e Divulgação"],
    "Preservação do Patrimônio Cultural": ["Conservação", "Restauração", "Documentação", "Educação e Disseminação"]
}

subcategorias = {
    "Digitalização": ["Scanner 3D", "Fotogrametria", "Impressão 3D"],
    "Armazenamento": ["Arquivos em Nuvem", "Bancos de Dados Digitais", "Repositórios Digitais"],
    "Software": ["Ferramentas de Restauração Digital", "Modelagem 3D", "Análise de Imagem", "Sistemas de Gerenciamento de Conteúdo"],
    "Acesso e Divulgação": ["Plataformas Online", "Realidade Virtual/Aumentada", "Exposições Virtuais", "Aplicativos Mobile"],
    "Conservação": ["Técnicas de Conservação Preventiva", "Monitoramento Ambiental", "Diagnóstico e Análise", "Conservação de Material Digital"],
    "Restauração": ["Métodos de Restauração Digital", "Integração de Técnicas Tradicionais e Digitais", "Estudos de Caso em Restauração", "Restauração de Áudio e Vídeo"],
    "Documentação": ["Metadados e Catalogação", "Sistemas de Documentação", "Normas e Padrões", "Fotografia e Documentação Gráfica"],
    "Educação e Disseminação": ["Programas Educacionais", "Treinamento e Capacitação", "Material Didático Digital", "Iniciativas de Engajamento Comunitário"]
}

# Calcular similaridades
similaridades = cosine_similarity(embeddings)

# Definir número de clusters
n_clusters = len(categorias["Tecnologia Digital"]) + len(categorias["Preservação do Patrimônio Cultural"])

# Agrupar embeddings em clusters
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(embeddings)
labels = kmeans.labels_

# Mapear clusters para categorias
categoria_mapping = {i: categoria for i, categoria in enumerate(categorias["Tecnologia Digital"]+ categorias["Preservação do Patrimônio Cultural"])}

# Atribuir categorias aos artigos
artigo_categorias = [categoria_mapping[label] for label in labels]

# Agrupar artigos em subcategorias
subcategoria_mappings = {}

for categoria in categorias["Tecnologia Digital"]+ categorias["Preservação do Patrimônio Cultural"]:
    categoria_indices = [i for i, cat in enumerate(artigo_categorias) if cat == categoria]
    categoria_embeddings = embeddings[categoria_indices]

    if len(categoria_embeddings) < 2:
        # Se há menos de 2 artigos, atribuí-los diretamente à subcategoria genérica
        subcategoria_mappings[categoria] = ["Geral"] * len(categoria_embeddings)
        continue

    # Definir número de subclusters
    n_subclusters = min(len(subcategorias[categoria]), len(categoria_embeddings))

    # Agrupar embeddings em subclusters
    kmeans_sub = KMeans(n_clusters=n_subclusters, random_state=0).fit(categoria_embeddings)
    sub_labels = kmeans_sub.labels_

    # Mapear subclusters para subcategorias
    subcategoria_mapping = {i: subcat for i, subcat in enumerate(subcategorias[categoria][:n_subclusters])}
    subcategoria_mappings[categoria] = [subcategoria_mapping[sub_label] for sub_label in sub_labels]

ontologia = defaultdict(lambda: defaultdict(list))

# Adicionar artigos à ontologia
for i, categoria in enumerate(artigo_categorias):
    subcategoria = subcategoria_mappings.get(categoria, ["Geral"])[i % len(subcategoria_mappings.get(categoria, ["Geral"]))]
    ontologia[categoria][subcategoria].append({
        "title": ids[i],
        "id": titles[i],
        "keywords": keywords[i],
        "author": autores[i],
        "properties": {
            "Tem_Tecnologia": categoria if categoria in categorias["Tecnologia Digital"] else None,
            "Tem_Armazenamento": subcategoria if categoria == "Armazenamento" else None,
            "Tem_Software": subcategoria if categoria == "Software" else None,
            "Tem_Acesso": subcategoria if categoria == "Acesso e Divulgação" else None,
            "Tem_Objetivo": None 
        }
    })

# Converter para um dicionário simples
ontologia_dict = {k: dict(v) for k, v in ontologia.items()}

# Exportar para JSON
with open('ontologia.json', 'w', encoding='utf-8') as f:
    json.dump(ontologia_dict, f, ensure_ascii=False, indent=4)
