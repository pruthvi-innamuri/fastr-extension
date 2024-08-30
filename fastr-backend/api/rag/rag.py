import chromadb
import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from sentence_transformers import SentenceTransformer
import httpx
from fastapi import HTTPException
from .chromahelpers import add_to_chroma, split_text, get_embedding_function, clear_database
    
chroma_client = chromadb.Client()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based on the following context and use general knowledge as last resort:

{context}

---

Answer the question based on the following context and use general knowledge as last resort: {question}
"""


def main():
    query_rag("What is the future of remote work?")

# call the internal LLM API (currently testing different models)
async def call_llm_api(prompt: str):
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

# query the DB and return the response from the LLM
async def query_rag(context: str, query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Add the context chunks to the DB.
    chunks = split_text(context)
    add_to_chroma(chunks)

    # Search the DB for the query text.
    results = db.similarity_search_with_score(query_text, k=5)

    # Create the prompt for the LLM.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Call the API asynchronously
    response_text = await call_llm_api(prompt)

    print([doc.page_content for doc, _ in sorted(results, key=lambda x: x[1])])
    # create the full response
    full_response = {
        "response": response_text,
        "sources": [doc.page_content for doc, _ in sorted(results, key=lambda x: x[1])] # Get the top 3 sources
    }

    # clear the database
    clear_database()

    # return the response and the sources
    return full_response

    # formatted_response = f"Response: {response_text}\n\nSources:"
    # for i, (doc, score) in enumerate(results, 1):
    #     source_content = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
    #     formatted_response += f"\n{i}. (Score: {score:.4f}) {source_content}"
    # print(formatted_response)
    # return response_text

if __name__ == "__main__":
    main()