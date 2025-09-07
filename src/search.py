from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import config
from models import create_embeddings, create_chat_model

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

# Configuração global do store de vetores
_store = None
_chain = None

def _get_store():
    """Inicializa o store de vetores se ainda não foi criado"""
    global _store
    if _store is None:
        embeddings = create_embeddings()
        _store = PGVector(
            embeddings=embeddings,
            collection_name=config.collection_name,
            connection=config.database_url,
            use_jsonb=True,
        )
    return _store

def _get_chain():
    """Inicializa a chain de busca se ainda não foi criada"""
    global _chain
    if _chain is None:
        llm = create_chat_model(temperature=0)
        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
        _chain = prompt | llm | StrOutputParser()
    return _chain

def search_documents(query, k=10):
    """Busca documentos similares à query fornecida"""
    store = _get_store()
    results = store.similarity_search_with_score(query, k=k)
    return results

def search_prompt(question, k=10):
    results = search_documents(question, k)
    
    if not results:
        return {
            'resposta': "Não foram encontrados documentos relevantes para sua pergunta.",
            'documentos_encontrados': 0,
            'contexto_usado': ""
        }
    
    # Extrair o contexto dos documentos encontrados
    contexto = ""
    for i, (doc, score) in enumerate(results, 1):
        contexto += f"DOCUMENTO {i} (relevância: {score:.3f}):\n"
        contexto += doc.page_content + "\n\n"
    
    # Gerar resposta usando o template
    chain = _get_chain()
    resposta = chain.invoke({
        "contexto": contexto,
        "pergunta": question
    })
    
    return {
        'resposta': resposta,
        'documentos_encontrados': len(results),
        'contexto_usado': contexto
    }