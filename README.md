# Sistema de Ingestão e Busca com IA

Um sistema flexível de ingestão de documentos PDF e busca semântica com suporte para múltiplos provedores de IA (OpenAI e Google).

## 🌟 Características Principais

- **Múltiplos Provedores**: Suporte completo para OpenAI e Google Gemini
- **Configuração Flexível**: Alternar facilmente entre provedores via variáveis de ambiente
- **Embedding e Chat Independentes**: Configure diferentes provedores para embedding e chat
- **Interface Conversacional**: Chat interativo para consultas aos documentos
- **Armazenamento Vetorial**: Utiliza PostgreSQL com pgvector para busca semântica

## 🚀 Como Executar

### 1. Configuração do Ambiente
```bash
cp .env.example .env
```
### 2. Instalação das Dependências

**Recomenda-se criar e ativar um ambiente virtual Python:**

```bash
python -m venv venv
source venv/bin/activate   
```

**Depois, instale as dependências:**

```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

Inicie o PostgreSQL com pgvector usando Docker:

```bash
docker-compose up -d
```

### 4. Ingestão do Documento

```bash
python src/ingest.py
```

### 5. Iniciar o Chat

```bash
python src/chat.py
```

## 📁 Estrutura do Projeto

```
src/
├── config.py      # Configuração centralizada
├── models.py      # Factory para modelos de IA
├── ingest.py      # Ingestão de documentos
├── search.py      # Busca semântica
└── chat.py        # Interface conversacional
```

---

> **Observacao:**  
> Os arquivos `config.py` e `models.py` foram adicionados para facilitar a alternância entre os modelos do Google e OpenAI, tornando a configuração e integração dos provedores mais simples e flexível.

