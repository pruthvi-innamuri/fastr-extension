from enum import Enum

INT_ENDPOINTS = {
    "llm_call": "/llm_call",
    "text_to_speech": "/text_to_speech",
}

EXT_ENDPOINTS = {
    'txt2speechstream': "https://api.elevenlabs.io/v1/text-to-speech/IKne3meq5aSn9XLyUdCD/stream",
    'txt2speech': "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
    'llm_call': "https://api.groq.com/openai/v1/chat/completions"
}

API_KEYS = {
    'text_to_speech': {
        'elevenlabs': ""
    },
    'llm_call': {
        'groq': "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"
    }
}

MODEL_PREFERENCES = {
    "llm_call": {
        "model": "llama3-70b-8192",
    },

    "text_to_speech": {
        "male": "IKne3meq5aSn9XLyUdCD",
        "female": "EXAVITQu4vr4xnSDxMaL",
        "stability": 0.4,
        "similarity_boost": 0.4,
        "model": "eleven_turbo_v2_5"
    }
}