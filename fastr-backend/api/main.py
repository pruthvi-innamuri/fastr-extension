import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import API_KEYS, EXT_ENDPOINTS, INT_ENDPOINTS, MODEL_PREFERENCES
from fastapi import FastAPI, HTTPException, Response, WebSocket
from fastapi.responses import StreamingResponse, FileResponse
import httpx
import websockets as ws
from models import LLMInput, TextToSpeechInput
import tempfile
import json
import base64
import asyncio
import pyaudio



app = FastAPI()

@app.get("/")
async def health_check():
    return "The health check is successful!"


@app.post("/llm_call")
async def api_call(llm_input: LLMInput):
    payload = {
        "messages": [
            {
                "role": "user",
                "content": llm_input.input_text,
            },
        ],
        "model": MODEL_PREFERENCES['llm_call']['model'],
    }

    print(payload)

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

@app.post("/text_to_speech_call")
async def text_to_speech(text_to_speech_input: TextToSpeechInput):

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
        
@app.websocket("/text_to_speech_websocket")
async def text_to_speech_websocket(websocket: WebSocket):
    # Initialize the connection with client
    await websocket.accept()

    voice_id = MODEL_PREFERENCES.get('text_to_speech').get('male')
    model = MODEL_PREFERENCES.get('text_to_speech').get('model')
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model}"


    # Function to handle the websocket connection with elevenlabs
    async def text_to_speech_websocket_call(uri):
        async with ws.connect(uri) as ws_connection:
            # Initialize the connection 
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
            await ws_connection.send(json.dumps(eos_message))

            # Added a loop to handle server responses and print the data received
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