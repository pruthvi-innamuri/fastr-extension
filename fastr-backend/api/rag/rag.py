from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from .helpers import add_to_chroma, split_text, get_embedding_function, clear_database, call_llm
from .__init__ import CHROMA_PATH, PROMPT_TEMPLATE
from typing import Union



async def query_rag(context: str, query_text: str) -> dict[str, Union[str, list[str]]]:
    """
    Function to query the RAG database and return the response from the LLM
    1. Prepare the DB.
    2. Search the DB for the query text.
    3. Create the prompt for the LLM.
    4. Call the API asynchronously
    5. Create the full response
    6. Clear the database
    7. Return the response and the sources
    """

    if context != '':
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        chunks = split_text(context)
        add_to_chroma(chunks)

        results = db.similarity_search_with_score(query_text, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        response_text = await call_llm(prompt)
        print([doc.page_content for doc, _ in sorted(results, key=lambda x: x[1])])
        full_response = {
            "response": response_text,
            "sources": [doc.page_content for doc, _ in sorted(results, key=lambda x: x[1])] # Get the top 3 sources
        }
    else:
        response_text = await call_llm(query_text)
        full_response = {
            "response": response_text,
            "sources": []
        }

    clear_database()

    return full_response