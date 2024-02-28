from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Qdrant
import json

with open("./config.json", "r") as c:
    config = json.load(c)

    API_KEY = config["OPENAI_KEY"]
    QDRANT_URL = config["QDRANT_URL"]
    EMBEDDING_NAME = config["EMBEDDING_NAME"]
    COLLECTION_NAME = config["COLLECTION_NAME"]


loader = CSVLoader("./fine-tuning/medquad.csv")
documents = loader.load()


embeddings = HuggingFaceBgeEmbeddings(
    model_name=EMBEDDING_NAME,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

qdrant = Qdrant.from_documents(
    documents,
    embeddings,
    url=QDRANT_URL,
    prefer_grpc=False,
    collection_name=COLLECTION_NAME
)

print("Database created!")