from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector
from config import config
from models import create_embeddings

docs = PyPDFLoader(str(config.pdf_path)).load()

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150, add_start_index=False).split_documents(docs)
if not splits:
    raise SystemExit(0)

enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in splits
]    

ids = [f"doc-{i}" for i in range(len(enriched))]

# Criar embeddings baseado no provedor configurado
embeddings = create_embeddings()

store = PGVector(
    embeddings=embeddings,
    collection_name=config.collection_name,
    connection=config.database_url,
    use_jsonb=True,
)

store.add_documents(documents=enriched, ids=ids)

def ingest_pdf():
    """Função principal para ingerir o PDF no banco de dados"""
    print(f"📄 Iniciando ingestão do PDF: {config.pdf_path}")
    print(f"🔧 Provedor de embeddings: {config.embedding_provider}")
    print(f"📊 Total de documentos processados: {len(enriched)}")
    print("✅ Ingestão concluída com sucesso!")


if __name__ == "__main__":
    ingest_pdf()