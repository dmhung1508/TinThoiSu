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
from database import Database
import config
from datetime import datetime
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
def add_text(doc, sourceLink,article_content):
    docs = []

    load_docs = Document(
        page_content= doc,
        metadata={
            "date": datetime.now().strftime("%d-%m-%Y"),
            "source_link" : sourceLink,
            "text": article_content,
            },
        
    )
    docs.append(load_docs)
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=uuids, show_progress=True)
def get_vector_store():
    return vector_store

def main():
    # db = Database(config, datetime.now())
    # dataCluster, dataArticle = db.get_all_article_only_web()
    # print(len(dataArticle))
    # # dataCluster.append([id_article, clean_text(text), clean_text(title), link])
    # # for i in tqdm(range(len(dataArticle))):
    # #     add_text(dataCluster[i][1], dataCluster[i][3], dataCluster[i][1], dataCluster[i][0])
    # for article in dataArticle:
    #     print(article)
    #     add_text(article['textContent'], article['link'], article['textContent'])
    results = vector_store.similarity_search(
        "donal Trump",
        k=10,
        # filter= []
    )
    response = [
        {"page_content": res.page_content, "metadata": res.metadata}
        for res in results
    ]
    print(response)

if __name__ == "__main__":
    main()