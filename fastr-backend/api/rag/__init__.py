import chromadb

chroma_client = chromadb.Client()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based on the following context (if provided) and use general knowledge as last resort:

{context}

---

Answer the question based on the above context (if provided) and use general knowledge as last resort: {question} Keep responseunder 300 characters!
"""