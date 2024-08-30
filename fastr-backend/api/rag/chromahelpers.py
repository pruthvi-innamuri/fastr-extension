import argparse
import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from sentence_transformers import SentenceTransformer



CHROMA_PATH = "chroma"

text = """Artificial Intelligence and Creativity
Artificial intelligence (AI) is increasingly being used to augment human creativity. From generating visual art to composing music, AI algorithms like GANs and transformers are enabling new forms of artistic expression. These technologies are not just tools; they are collaborators that can inspire and challenge artists to push their boundaries. While some fear that AI might replace human creativity, many believe that it will instead open up new possibilities for creative exploration.

The Future of Remote Work
The COVID-19 pandemic has permanently changed the landscape of work, making remote work more commonplace. Companies have adapted to this shift by implementing flexible work policies, allowing employees to work from anywhere. This trend has not only broadened the talent pool for employers but also given workers more control over their work-life balance. However, it has also raised challenges, such as maintaining company culture and ensuring effective communication among remote teams.

Renewable Energy Innovations
Renewable energy is rapidly advancing, with solar, wind, and hydroelectric power leading the way. Innovations in energy storage, like battery technology, are making renewable sources more reliable and viable on a large scale. Governments and companies worldwide are investing heavily in clean energy to combat climate change and reduce reliance on fossil fuels. As technology improves, the cost of renewable energy continues to decrease, making it an increasingly attractive option for both consumers and businesses.

Quantum Computing Potential
Quantum computing is poised to revolutionize industries by solving problems that are currently intractable for classical computers. Unlike traditional computers, which use bits, quantum computers use qubits that can exist in multiple states simultaneously, vastly increasing their computational power. This technology has the potential to transform fields such as cryptography, material science, and drug discovery. However, practical quantum computing is still in its infancy, with significant challenges remaining before it can be widely implemented.

Mental Health Awareness
In recent years, mental health awareness has gained significant momentum, breaking down stigmas and encouraging open conversations. More people are recognizing the importance of mental well-being and seeking help when needed. This shift is supported by increased access to resources, such as therapy and counseling services, often available online. As society continues to prioritize mental health, the hope is that future generations will grow up in a world where mental well-being is as important as physical health.

Space Exploration Milestones
Space exploration has seen remarkable milestones in the past decade, with private companies like SpaceX leading the charge. The successful deployment of reusable rockets has significantly reduced the cost of space travel, making it more accessible. Additionally, missions to Mars, the Moon, and beyond are being planned with the goal of establishing human presence on other planets. These advancements bring humanity closer to understanding the universe and potentially finding extraterrestrial life."""

def main():

    # Clear the database if it exists
    clear_database()

    # Create the data store
    chunks = split_text(text)
    add_to_chroma(chunks)

    # Print a few database items
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    items = db.get(limit=3)
    print("\nSample database items:")
    for i, item in enumerate(items['documents'], 1):
        print(f"\nItem {i}:")
        print(f"Content: {item[:100]}...")  # Print first 100 characters
        print(f"ID: {items['ids'][i-1]}")


# get the embedding function for the DB
def get_embedding_function():
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    class EmbeddingFunction:
        def embed_documents(self, texts):
            return model.encode(texts).tolist()
        def embed_query(self, text):
            return model.encode(text).tolist()
    
    return EmbeddingFunction()

def split_text(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)


def add_to_chroma(chunks: list[str]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Create Document objects from text chunks
    documents = [Document(page_content=chunk, metadata={}) for chunk in chunks]

    # Generate unique IDs for each chunk
    chunk_ids = [f"chunk_{i}" for i in range(len(documents))]

    # Add the documents to the database
    print(f"👉 Adding new documents: {len(documents)}")
    db.add_documents(documents, ids=chunk_ids)
    db.persist()

    print(f"✅ Added {len(documents)} new documents to the database")


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()