from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from tqdm import tqdm
from langchain_core.documents import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Khởi tạo embeddings
embeddings = HuggingFaceEmbeddings(
    model_name='hiieu/halong_embedding',
)

# Khởi tạo Chroma client sử dụng HttpClient
client = chromadb.PersistentClient()

# Kết nối tới server Chroma thông qua client
vector_store = Chroma(
    collection_name="news",
    embedding_function=embeddings,
    client=client
)
def add_text(doc,date, sourceLink,article_content):
    docs = []
    load_docs = Document(
        page_content= doc,
        metadata={
            "date": date,
            "source_link" : sourceLink,
            "text": article_content,
            },
        
    )
    docs.append(load_docs)
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=uuids, show_progress=True)
def get_vector_store():
    return vector_store