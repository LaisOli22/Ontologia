from rdflib import Graph, URIRef, Literal, RDF, RDFS, OWL
from rdflib.namespace import SKOS
import json

# Carregar a ontologia JSON
with open('ontologia.json', 'r', encoding='utf-8') as f:
    ontologia = json.load(f)

# Criar um grafo RDF
g = Graph()

# Definir um namespace
ns = {
    'ont': URIRef('http://example.org/ontology#')
}

# Adicionar categorias e subcategorias ao grafo
for categoria, subcategorias in ontologia.items():
    categoria_uri = ns['ont'] + categoria.replace(" ", "_")
    
    g.add((categoria_uri, RDF.type, OWL.Class))
    g.add((categoria_uri, RDFS.label, Literal(categoria)))
    
    for subcategoria, artigos in subcategorias.items():
        subcategoria_uri = ns['ont'] + subcategoria.replace(" ", "_")
   
        g.add((subcategoria_uri, RDF.type, OWL.Class))
        g.add((subcategoria_uri, RDFS.label, Literal(subcategoria)))
    
        g.add((subcategoria_uri, RDFS.subClassOf, categoria_uri))
        
        for artigo in artigos:
            artigo_uri = ns['ont'] + artigo['id'].replace(" ", "_")
            
            # Adicionar o artigo
            g.add((artigo_uri, RDF.type, OWL.NamedIndividual))
            g.add((artigo_uri, RDFS.label, Literal(artigo['title'])))
            g.add((artigo_uri, SKOS.note, Literal("Keywords: " + ", ".join(artigo['keywords']))))
            g.add((artigo_uri, SKOS.note, Literal("Author: " + artigo['author'])))
            
            # Relação entre artigo e subcategoria
            g.add((artigo_uri, RDFS.subClassOf, subcategoria_uri))
            
            # Adicionar propriedades
            for prop, value in artigo['properties'].items():
                if value:
                    prop_uri = ns['ont'] + prop.replace(" ", "_")
                    g.add((artigo_uri, URIRef(prop_uri), Literal(value)))

# Salvar o grafo como um arquivo OWL
g.serialize(destination='grafo.owl', format='xml')

print("Ontologia OWL gerada com sucesso.")
