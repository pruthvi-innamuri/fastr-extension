import { apiCall } from './apicalls';

// Handlers for the popup

const getResponseHandler = async (inputText: string, setApiResponse: (response: string) => void) => {
    console.log('Getting response');
    const response = await apiCall(inputText);
    setApiResponse(response || 'Error occurred while fetching data.');
  };

const saveHandler = (inputText: string, apiResponse: string, setInputText: (text: string) => void, setApiResponse: (response: string) => void) => {
    console.log('Saving response');
    chrome.storage.local.get(['savedResponses'], (result) => {
        const savedResponses = result.savedResponses || [];
        savedResponses.push({ question: inputText, response: apiResponse });
        chrome.storage.local.set({ savedResponses }, () => {
        console.log(savedResponses);
        });
    });
    // Clear the input and API response
    setInputText('');
    setApiResponse('');
    chrome.storage.local.set({ current_selection: '' }, () => {});
};

const clearHandler = (setInputText: (text: string) => void, setApiResponse: (response: string) => void) => {
    console.log('Clearing all responses');
    chrome.storage.local.set({ savedResponses: [] }, () => {
        console.log('Cleared all saved responses');
    });

    // Clear input and API response
    setInputText('');
    setApiResponse('');
    chrome.storage.local.set({ current_selection: '' }, () => {});
};

const downloadHandler = (setApiResponse: (response: string) => void) => {
    console.log('Downloading saved responses');
    chrome.storage.local.get(['savedResponses'], (result) => {
        const savedResponses = result.savedResponses || [];
        if (savedResponses.length === 0) {
        console.log('No saved responses to download');
        setApiResponse('No saved responses to download');
        return;
        }

        let fileContent = '';
        savedResponses.forEach((item: any, index: number) => {
        fileContent += `Question ${index + 1}: \n`;
        fileContent += `-------------------------------\n`;
        fileContent += `${item.question}\n\n`;
        fileContent += `Response ${index + 1}: \n`;
        fileContent += `-------------------------------\n`;
        fileContent += `${item.response}\n\n\n\n`;
        });

        const blob = new Blob([fileContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'saved_responses.txt';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    });
};
const textToSpeechHandler = async (text: string, setApiResponse: (response: string) => void) => {
  console.log('Converting text to speech');
  const payload = {
    input_text: text,
    voice_type: 'default' // You can change this if you want to support different voice types
  };

  try {
    const response = await fetch('http://localhost:8000/text_to_speech_call', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    
    const audio = new Audio(audioUrl);
    audio.play();

  } catch (error) {
    console.error('Error:', error);
    setApiResponse(`Error converting text to speech: ${error}`);
  }
};

const textToSpeechSocketHandler = async (text: string, setApiResponse: (response: string) => void) => {
    console.log('Converting text to speech');
    const payload = {
      input_text: text,
      voice_type: 'default' // You can change this if you want to support different voice types
    };
  
    try {
        const socket = new WebSocket('ws://127.0.0.1:8000/text_to_speech_websocket');
        //const audioQueue: HTMLAudioElement[] = [];
        //let isPlaying = false;

        socket.onopen = () => {
            console.log('WebSocket connection opened');
            socket.send(JSON.stringify(payload));
        };


        const audioQueue: AudioBuffer[] = [];
        let isPlaying = false;
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();

        socket.onmessage = async (event) => {
            console.log('WebSocket message received:', event.data);
        
            // Assuming the server sends the audio data as binary data
            const arrayBuffer = await event.data.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        
            audioQueue.push(audioBuffer);
            if (!isPlaying) {
                playNextInQueue();
            }
        };
        
        const playNextInQueue = () => {
            if (audioQueue.length === 0) {
                isPlaying = false;
                return;
            }
        
            isPlaying = true;
            console.log("audioQueue.length", audioQueue.length);
            const audioBuffer = audioQueue.shift();
        
            if (audioBuffer) {
                const source = audioContext.createBufferSource();
                source.buffer = audioBuffer;
                source.connect(audioContext.destination);
        
                source.onended = () => {
                    playNextInQueue();
                };
        
                source.start(0); // Start playing the audio buffer immediately
            } else {
                isPlaying = false;
            }
        };

        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            setApiResponse(`Error converting text to speech: ${error}`);
        };

        socket.onclose = () => {
            console.log('WebSocket connection closed');
        };
    } catch (error) {
        console.error('Error:', error);
        setApiResponse(`Error converting text to speech: ${error}`);
    }
};


const clearSelectionHandler = (setInputText: (text: string) => void, setApiResponse: (response: string) => void) => {
    setInputText('');
    setApiResponse('');
    chrome.storage.local.set({ current_selection: '' }, () => {});
};


export { getResponseHandler, saveHandler, clearHandler, downloadHandler, textToSpeechHandler, textToSpeechSocketHandler, clearSelectionHandler };