# Ontologia
1. Criar um diretório com os pdfs baixados
2. Criar um arquivo JSON com os metadados dos pdfs(corpo textual)
   - usei a biblioteca PyMuPDF. Essas biblioteca permite a extração de informações dos PDFs, como título, autor e data de publicação
   - o arquivo criado  foi o 'pdf_metadata.json'
3. Extração de features com o HuggingFace
   - Eu apliquei o modelo de feature extraction da Hugging Face 'YituTech/conv-bert-base' pra carregar o corpo textual JSON
   - o arquivo criado  foi o 'pdf_metadata_with_features.json'
4. Criar uma ontologia
   - Carregar o arquivo JSON com as features para extrair as informações relevantes
   - Definir uma ontologia para categorizar as disciplinas abordadas nos artigos
   - o arquivo criado  foi o 'ontologia.json'
5. Criar um grafo
   - Carregar o arquivo json da Ontologia
   - Adicionar as categorias, subcategorias e relações
   - o arquivo criado  foi o 'grafo.owl'
6. Com o arquivo .owl criado dá pra colocar em um software pra exibir graficamente como o Web Protegè. Eu preferi colocar em um software chamado Gephi, aí precisa converter o arquivo pra graphml
   - Carregar o arquivo json da Ontologia
   - Adicionar as categorias, subcategorias e relações
   - o arquivo criado  foi o 'grafo.graph'
   - Importar no Gephi e ajustar os detalhes
