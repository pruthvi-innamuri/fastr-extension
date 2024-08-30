import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import API_KEYS, EXT_ENDPOINTS, MODEL_PREFERENCES
from fastapi import FastAPI, HTTPException, Response, WebSocket
from fastapi.responses import FileResponse
import httpx
import websockets as ws
from models import LLMInput, TextToSpeechInput, RAGInput
import tempfile
import json
import base64
from rag.rag import query_rag
from typing import Union



app = FastAPI()

@app.get("/")
async def health_check() -> str:
    return "The health check is successful!"

@app.get("/api_keys")
async def get_api_keys() -> dict[str, str]:
    return API_KEYS


@app.post("/llm_call")
async def api_call(llm_input: LLMInput) -> dict[str, str]:
    """
    Function to handle the LLM call
    """
    payload = {
        "messages": [
            {
                "role": "user",
                "content": llm_input.input_text,
            },
        ],
        "model": MODEL_PREFERENCES['llm_call']['model'],
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                EXT_ENDPOINTS['llm_call'],
                json=payload,
                headers={
                    "Authorization": f"Bearer {API_KEYS['llm_call']['groq']}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            print(content)
            return {"response": content}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        


@app.post("/rag_call")
async def rag_call(rag_input: RAGInput) -> dict[str, Union[str, list[str]]]:
    """
    Function to handle the RAG call
    """
    full_response = await query_rag(rag_input.context, rag_input.query_text)
    return full_response


@app.post("/text_to_speech_call")
async def text_to_speech(text_to_speech_input: TextToSpeechInput) -> FileResponse:
    """
    Function to handle the text to speech call
    1. Prepare the request
    2. Send and process the request
    3. Return the response
    """

    voice_id = MODEL_PREFERENCES.get('text_to_speech').get('female')
    uri = EXT_ENDPOINTS.get('txt2speech').replace('{voice_id}', voice_id)
    params = {"enable_logging": "true"}
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": API_KEYS.get('text_to_speech').get('elevenlabs')
    }
    payload = {
        "text": text_to_speech_input.input_text,
        "voice_settings": {
            "stability": MODEL_PREFERENCES.get('text_to_speech').get('stability'),
            "similarity_boost": MODEL_PREFERENCES.get('text_to_speech').get('similarity_boost')
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(uri, params=params, headers=headers, json=payload)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name
            
            return FileResponse(tmp_file_path, media_type="audio/mpeg", filename="output.mp3")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
# lower latency approach using websockets
@app.websocket("/text_to_speech_websocket")
async def text_to_speech_websocket(websocket: WebSocket, t2s_input: TextToSpeechInput) -> None:
    """
    Initialize the connection with client
    Function to handle the websocket connection with elevenlabs
    Send the audio in chunks (while loop)
    Close the connection
    """


    await websocket.accept()

    voice_id = MODEL_PREFERENCES.get('text_to_speech').get(t2s_input.voice_type)
    model = MODEL_PREFERENCES.get('text_to_speech').get('model')
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model}"


    async def text_to_speech_websocket_call(uri) -> None:        
        async with ws.connect(uri) as ws_connection:
            bos_message = {
                "text": " ",
                "voice_settings": {
                    "stability": 0.5,
                "similarity_boost": 0.8
            },
                "xi_api_key": API_KEYS.get('text_to_speech').get('elevenlabs')
            }
            await ws_connection.send(json.dumps(bos_message))

            input_message = {
                "text": "this is a really long piece of text that I am writing in order to test how well the websocket connection is and whether it is only sending one audio chunk or everything except for the last one. I think this message could be the reason why the audio is not being generated properly. I am not sure if it is because of the length of the message or the message itself.",
                "try_trigger_generation": True
            }
            await ws_connection.send(json.dumps(input_message))
            
            eos_message = {
                "text": ""
            }
            await ws_connection.send(json.dumps({eos_message}))

            while True:
                try:
                    response = await ws_connection.recv()
                    data = json.loads(response)
                    print("Server response:", data)
    
                    if data["audio"]:
                        chunk = base64.b64decode(data["audio"])
                        print("Received audio chunk")
                        await websocket.send_bytes(chunk)
                    else:
                        print("No audio data in the response")
                        break
                except ws.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break

    await text_to_speech_websocket_call(uri)
    await websocket.close()

@app.post("/pass-api-keys")
async def pass_api_keys(api_keys: dict) -> dict[str, str]:
    """

    Function to update the API keys in the API_KEYS dictionary
    Check if the keys are present and valid
    Update the API_KEYS dictionary
    Return a success message

    """

    try:
        groq_api_key = api_keys.get("groq")
        elevenlabs_api_key = api_keys.get("elevenlabs")

        if not groq_api_key or not elevenlabs_api_key:
            raise HTTPException(status_code=400, detail="Both Groq and ElevenLabs API keys are required")

        async def test_groq_api():
            test_payload = {
                "messages": [{"role": "user", "content": "Hello"}],
                "model": MODEL_PREFERENCES['llm_call']['model'],
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        EXT_ENDPOINTS['llm_call'],
                        json=test_payload,
                        headers={"Authorization": f"Bearer {groq_api_key}"},
                        timeout=10.0
                    )
                    response.raise_for_status()
                    return True
                except httpx.HTTPStatusError:
                    return False

        async def test_elevenlabs_api():
            test_payload = {
                "text": "Test",
                "voice_id": MODEL_PREFERENCES['text_to_speech']['male'],
                "model_id": MODEL_PREFERENCES['text_to_speech']['model']
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        EXT_ENDPOINTS['txt2speech'].format(voice_id=MODEL_PREFERENCES['text_to_speech']['male']),
                        json=test_payload,
                        headers={"xi-api-key": elevenlabs_api_key},
                        timeout=10.0
                    )
                    response.raise_for_status()
                    return True
                except httpx.HTTPStatusError:
                    return False

        groq_valid = await test_groq_api()
        elevenlabs_valid = await test_elevenlabs_api()

        if not groq_valid:
            raise HTTPException(status_code=400, detail="Invalid Groq API key")
        if not elevenlabs_valid:
            raise HTTPException(status_code=400, detail="Invalid ElevenLabs API key")
        
        API_KEYS['llm_call']['groq'] = groq_api_key
        API_KEYS['text_to_speech']['elevenlabs'] = elevenlabs_api_key
        return {"message": "API keys updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating API keys: {str(e)}")