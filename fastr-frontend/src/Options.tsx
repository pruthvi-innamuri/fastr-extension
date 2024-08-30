
import './Options.css'
import { saveApiKeysHandler } from './utils/handlers'

function Options() {
  return (
    <div className="options-container">
      <h1 className="text-2xl font-bold mb-4">API Key Settings</h1>
      <form className="space-y-6" onSubmit={(e) => {
        e.preventDefault();
        const groqApiKey = (document.getElementById('groqApiKey') as HTMLInputElement).value;
        const elevenLabsApiKey = (document.getElementById('elevenLabsApiKey') as HTMLInputElement).value;
        saveApiKeysHandler(groqApiKey, elevenLabsApiKey)
          .then((apiResponse) => {
            alert(apiResponse.message);
          })
          .catch((error) => {
            alert(`Error saving API keys: ${error}`);
          });
      }}>
        <div className="flex flex-col items-start mb-3">
          <div>
            <label htmlFor="groqApiKey" className="text-lg font-medium mb-2">
              Groq API Key
            </label>
          </div>
          <input
            type="password"
            id="groqApiKey"
            name="groqApiKey"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="Enter your Groq API key"
            style={{ width: '100%' }}
          />
        </div>

        <div className="flex flex-col items-start">
          <div>
            <label
              htmlFor="elevenLabsApiKey"
              className="text-sm font-medium mb-2"
            >
              ElevenLabs API Key
            </label>
          </div>
          <input
            type="password"
            id="elevenLabsApiKey"
            name="elevenLabsApiKey"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="Enter your ElevenLabs API key"
            style={{ width: '100%' }}
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 mt-4 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          style={{ width: '100%' }}
        >
          Save
        </button>
      </form>
    </div>
  )
}

export default Options
