import json
from datasets import Dataset
from transformers import AutoTokenizer, AutoModel
import torch

# Carregar o dataset JSON
with open('pdf_metadata.json') as f:
    data = json.load(f)

# Converter o dataset para o formato Hugging Face Dataset
dataset = Dataset.from_list(data)

# Inicializar o tokenizer e o modelo da Hugging Face para YituTech/conv-bert-base
tokenizer = AutoTokenizer.from_pretrained('YituTech/conv-bert-base')
model = AutoModel.from_pretrained('YituTech/conv-bert-base')

# Tokenizar e extrair embeddings
def extract_features(examples):
    inputs = tokenizer(examples['title'], padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    # Usar a representação do [CLS] token (primeira posição)
    cls_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return {'embeddings': cls_embeddings}

# Aplicar a extração de features ao dataset
features = dataset.map(extract_features, batched=True)
print(features)

# Salvar as features extraídas em um arquivo JSON
features.to_json('pdf_metadata_with_features.json')

