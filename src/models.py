from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from config import config

def create_embeddings():
    """Cria o objeto de embeddings baseado no provedor configurado"""
    if config.embedding_provider == "openai":
        print(f"🔧 Usando OpenAI Embeddings: {config.get_embedding_model_name()}")
        return OpenAIEmbeddings(
            model=config.get_embedding_model_name(),
            api_key=config.openai_api_key
        )
    elif config.embedding_provider == "google":
        print(f"🔧 Usando Google Embeddings: {config.get_embedding_model_name()}")
        return GoogleGenerativeAIEmbeddings(
            model=config.get_embedding_model_name(),
            google_api_key=config.google_api_key
        )
    else:
        raise ValueError(f"Provedor de embedding não suportado: {config.embedding_provider}")

def create_chat_model(temperature=0):
    """Cria o modelo de chat baseado no provedor configurado"""
    if config.chat_provider == "openai":
        print(f"🔧 Usando OpenAI Chat: {config.get_chat_model_name()}")
        return ChatOpenAI(
            model=config.get_chat_model_name(),
            temperature=temperature,
            api_key=config.openai_api_key
        )
    elif config.chat_provider == "google":
        print(f"🔧 Usando Google Chat: {config.get_chat_model_name()}")
        return ChatGoogleGenerativeAI(
            model=config.get_chat_model_name(),
            temperature=temperature,
            google_api_key=config.google_api_key
        )
    else:
        raise ValueError(f"Provedor de chat não suportado: {config.chat_provider}")
