import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from sentence_transformers import SentenceTransformer
import httpx
from fastapi import HTTPException
from .__init__ import CHROMA_PATH


def get_embedding_function() -> SentenceTransformer:
    """
    embedding function callback for the DB
    """
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    class EmbeddingFunction:
        def embed_documents(self, texts):
            if not texts:
                return []
            return model.encode(texts).tolist()
        def embed_query(self, text):
            if not text:
                return []
            return model.encode(text).tolist()
    
    return EmbeddingFunction()

def split_text(text: str) -> list[str]:
    """
    Split the text into chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)

def add_to_chroma(chunks: list[str]) -> None:
    """
    Add the chunks to the DB
    1. Load the existing database.
    2. Create Document objects from text chunks
    3. Generate unique IDs for each chunk
    4. Add the documents to the database
    5. Persist the database
    """

    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    documents = [Document(page_content=chunk, metadata={}) for chunk in chunks]

    chunk_ids = [f"chunk_{i}" for i in range(len(documents))]

    print(f"👉 Adding new documents: {len(documents)}")
    db.add_documents(documents, ids=chunk_ids)
    db.persist()

    print(f"✅ Added {len(documents)} new documents to the database")


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


async def call_llm(prompt: str) -> str:
    """
    Call the LLM asynchronously
    """
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "model": "mixtral-8x7b-32768",  # Assuming this is the model specified in MODEL_PREFERENCES
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/llm_call",  # Assuming the API is running locally
                json={"input_text": prompt},
                headers={
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            content = response.json()["response"]
            return content
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))