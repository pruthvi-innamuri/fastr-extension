from pydantic import BaseModel

class LLMInput(BaseModel):
    input_text: str

class TextToSpeechInput(BaseModel):
    input_text: str
    voice_type: str