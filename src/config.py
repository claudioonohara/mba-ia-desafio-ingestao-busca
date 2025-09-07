import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

for k in ("EMBEDDING_PROVIDER", "CHAT_PROVIDER", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", 
          "PDF_PATH",
          "OPENAI_EMBEDDING_MODEL","OPENAI_CHAT_MODEL","OPENAI_API_KEY",
          "GOOGLE_EMBEDDING_MODEL","GOOGLE_CHAT_MODEL", "GOOGLE_API_KEY"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

# Tipos para validação
EmbeddingProvider = Literal["openai", "google"]
ChatProvider = Literal["openai", "google"]

class Config:
    """Configuração centralizada para provedores de embedding e chat"""
    
    def __init__(self):
        # Configuração dos provedores
        self.embedding_provider: EmbeddingProvider = os.getenv("EMBEDDING_PROVIDER").lower()
        self.chat_provider: ChatProvider = os.getenv("CHAT_PROVIDER").lower()
        
        # Configurações gerais
        self.database_url = os.getenv("DATABASE_URL")
        self.collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
        self.pdf_path = os.getenv("PDF_PATH")
        
        # Configurações de embedding
        self.openai_embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL")
        self.google_embedding_model = os.getenv("GOOGLE_EMBEDDING_MODEL")
        
        # Configurações de chat
        self.openai_chat_model = os.getenv("OPENAI_CHAT_MODEL")
        self.google_chat_model = os.getenv("GOOGLE_CHAT_MODEL")
        
        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        # Validar variáveis obrigatórias
        self._validate_required_vars()
    
    def _validate_required_vars(self):
        """Valida se todas as variáveis necessárias estão definidas"""
        required_vars = ["DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"]
        
        # Adicionar variáveis específicas do provedor de embedding
        if self.embedding_provider == "openai":
            required_vars.extend(["OPENAI_API_KEY"])
        elif self.embedding_provider == "google":
            required_vars.extend(["GOOGLE_API_KEY"])
        
        # Adicionar variáveis específicas do provedor de chat
        if self.chat_provider == "openai":
            required_vars.extend(["OPENAI_API_KEY"])
        elif self.chat_provider == "google":
            required_vars.extend(["GOOGLE_API_KEY"])
        
        # Remover duplicatas
        required_vars = list(set(required_vars))
        
        # Verificar se todas estão definidas
        for var in required_vars:
            if not os.getenv(var):
                raise RuntimeError(f"Variável de ambiente {var} não está definida")
    
    def get_embedding_model_name(self) -> str:
        """Retorna o nome do modelo de embedding baseado no provedor"""
        if self.embedding_provider == "openai":
            return self.openai_embedding_model
        elif self.embedding_provider == "google":
            return self.google_embedding_model
        
    def get_chat_model_name(self) -> str:
        """Retorna o nome do modelo de chat baseado no provedor"""
        if self.chat_provider == "openai":
            return self.openai_chat_model
        elif self.chat_provider == "google":
            return self.google_chat_model
    
    def print_config(self):
        """Imprime a configuração atual"""
        print("=== Configuração Atual ===")
        print(f"Provedor de Embedding: {self.embedding_provider}")
        print(f"Modelo de Embedding: {self.get_embedding_model_name()}")
        print(f"Provedor de Chat: {self.chat_provider}")
        print(f"Modelo de Chat: {self.get_chat_model_name()}")
        print(f"Coleção do Banco: {self.collection_name}")
        print("=" * 27)

# Instância global da configuração
config = Config()
