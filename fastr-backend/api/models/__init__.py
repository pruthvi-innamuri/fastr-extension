from pydantic import BaseModel

class LLMInput(BaseModel):
    input_text: str

class TextToSpeechInput(BaseModel):
    input_text: str
    voice_type: str

class RAGInput(BaseModel):
    context: str
    query_text: str