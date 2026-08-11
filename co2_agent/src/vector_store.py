import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def create_vector_store(tips_file=os.path.join(os.path.dirname(__file__), '..', 'data', 'tips.txt'), collection_name='sustainability_tips'):
    # Create Chroma client
    client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), '..', 'data', 'chroma_db'))

    # Create or get collection
    collection = client.get_or_create_collection(name=collection_name)

    # Check if collection already has data to avoid re-embedding
    if collection.count() > 0:
        # Initialize embedding model (needed for queries)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return collection, model

    # Load tips
    with open(tips_file, 'r') as f:
        text = f.read()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)

    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Embed and add to collection
    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        embeddings=embeddings,
        documents=chunks,
        ids=ids
    )

    return collection, model

if __name__ == "__main__":
    create_vector_store()
