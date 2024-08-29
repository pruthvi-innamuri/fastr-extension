import './App.css'
import { useEffect, useState } from 'react'
import { getResponseHandler, saveHandler, clearHandler, downloadHandler, textToSpeechSocketHandler, clearSelectionHandler } from './utils/handlers';
import ArrowUpOnSquareIcon from '@heroicons/react/24/outline/ArrowUpOnSquareIcon'; // Export Icon
import { PaperAirplaneIcon } from '@heroicons/react/16/solid'; // send icon
import BookmarkIcon from '@heroicons/react/24/outline/BookmarkIcon'; // save icon
import TrashIcon from '@heroicons/react/24/outline/TrashIcon'; // clear icon
import SpeakerWaveIcon from '@heroicons/react/24/outline/SpeakerWaveIcon'; // listen icon
import BackspaceIcon from '@heroicons/react/24/outline/BackspaceIcon'; // backspace icon
import { updateInputText } from './utils/helpers';

function App() {
  console.log('App loaded');

  const [inputText, setInputText] = useState('');
  const [apiResponse, setApiResponse] = useState('');


  // when the popup is triggered
  useEffect(() => {
    updateInputText(setInputText);
    const port = chrome.runtime.connect({ name: 'popup' });
    chrome.runtime.onMessage.addListener(
      function(request, _sender, sendResponse) {
          if (request.action === "NewTextSelected") {
            updateInputText(setInputText);
            sendResponse({ success: true });
          }
      }
    );

    return () => {
      console.log('disconnecting port');
      port.disconnect();
    };
  }, []);
  
  // Update current_selection whenever inputText changes
  useEffect(() => {
    chrome.storage.local.set({ current_selection: inputText }, () => {
      console.log('current_selection set to', inputText);
    });
  }, [inputText]);


  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-8 text-blue-600">Fastr</h1>
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <textarea 
          value={inputText} 
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your message here"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-4 h-32 resize-y"
        />

        <button
          onClick={() => getResponseHandler(inputText, setApiResponse)}
          className="flex items-center justify-center p-2"
          title="Send"
        >
          <PaperAirplaneIcon className="text-white" style={{ display: 'block', height: '2rem', width: '2rem' }}/> 
        </button>
        <button 
          onClick={() => saveHandler(inputText, apiResponse, setInputText, setApiResponse)}
          className="flex items-center justify-center p-2 ml-2 mr-1"
          title="Save"
        >
          <BookmarkIcon className="text-white" style={{ display: 'block', height: '2rem', width: '2rem' }}/>
        </button>

        <button 
          onClick={() => textToSpeechSocketHandler(apiResponse, setApiResponse)}
          className="flex items-center justify-center p-2 mt-2 ml-1 mr-2"
          title="Listen"
        >        
          <SpeakerWaveIcon className="text-white" style={{ display: 'block', height: '2rem', width: '2rem' }}/>
        </button>

        <button 
          onClick={() => clearSelectionHandler(setInputText, setApiResponse)}
          className="flex items-center justify-center p-2 mt-2"
          title="Clear"
        >        
          <BackspaceIcon className="text-white" style={{ display: 'block', height: '2rem', width: '2rem' }}/>
        </button>


        <div className="mt-4 text-gray-600 max-h-40 overflow-y-auto bg-gray-100 p-3 rounded">
          {apiResponse || 'Response will appear here'}
        </div>


        <button 
          onClick={() => downloadHandler(setApiResponse)}
          className="flex items-center justify-center p-2"
          title="Download Conversations"
        >        
          <ArrowUpOnSquareIcon className="text-white" style={{ display: 'block', height: '2rem', width: '2rem' }}/>
        </button>

        <button 
          onClick={() => clearHandler(setInputText, setApiResponse)}
          className="flex items-center justify-center p-2 ml-1 mr-2"
          title="Clear All Conversations"
        >
          <TrashIcon className="text-white" style={{ display: 'block', height: '2rem', width: '2rem' }}/>
        </button>

      </div>
    </div>
  )
}

export default App