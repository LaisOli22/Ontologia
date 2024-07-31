import json
import networkx as nx

# Carregar o arquivo JSON
with open('ontologia.json', 'r', encoding='utf-8') as f:
    ontologia = json.load(f)

# Criar um grafo direcionado
G = nx.DiGraph()

# Adicionar nós e arestas ao grafo
for categoria, subcategorias in ontologia.items():
    G.add_node(categoria, type='Categoria')
    
    for subcategoria, artigos in subcategorias.items():
        G.add_node(subcategoria, type='Subcategoria')
        G.add_edge(categoria, subcategoria, relationship='contains')
        
        for artigo in artigos:
            G.add_node(artigo["title"], type='Artigo', author=artigo["author"], keywords=", ".join(artigo["keywords"]))
            G.add_edge(subcategoria, artigo["title"], relationship='contains')

# Exportar para GraphML
nx.write_graphml(G, 'grafo.graphml')
