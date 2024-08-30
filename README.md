# Fastr 💨

### Speed Up Your Browser Workflow

**Fastr** is a Chrome extension designed to streamline your browsing experience. With Fastr, you can quickly access a powerful LLM chatbox by simply highlighting text on any webpage and pressing the `Tab` key. This tool uses Retrieval-Augmented Generation (RAG) to surface the most accurate and relevant information from the entire open webpage.

## Purpose

The primary goal of **Fastr** is to enhance productivity by reducing the time and effort needed to retrieve information and interact with content on the web. Whether you're researching, writing, or just browsing, Fastr ensures that you have the most pertinent information at your fingertips, enabling you to work faster and smarter.

## Features

- **Highlight & Trigger**: Highlight any text on a webpage and press `Tab` to open the Fastr chatbox.
- **LLM Integration**: The chatbox leverages an advanced language model to provide context-aware responses.
- **RAG-Powered**: Utilizes Retrieval-Augmented Generation (RAG) to pull in the most relevant content from the entire webpage.
- **Session Persistence**: Save your questions and responses between browsing sessions, allowing you to pick up where you left off.
- **Export to txt**: Easily export all your questions and responses from a session into a `.txt` file for documentation or future reference.
- **Seamless Browser Integration**: Designed to work effortlessly within your Chrome browser.

## Demo

Check out a quick demo of Fastr in action:

https://github.com/user-attachments/assets/c524ef86-cd62-42cb-9f6e-7374eed60dae


## Implementation

### Frontend Architecture

#### Tools
The frontend is built using **React**, **TypeScript**, and **Vite**:

- **React**: Enables modular, reusable UI components.
- **TypeScript**: Adds type safety, reducing errors and improving development.
- **Vite**: Fast build tool that transpiles TypeScript and JSX into the HTML, CSS, and JavaScript needed for Chrome extensions.

#### Systems Overview
<img width="746" alt="Screenshot 2024-08-30 at 1 00 28 PM" src="https://github.com/user-attachments/assets/28ceb971-b80c-4910-9617-5b074c560df5">

#### Chrome Extension API & Runtimes
Chrome extensions have three distinct JavaScript runtimes:

1. **Content Scripts**: Run within web pages, allowing DOM manipulation.
2. **Background Scripts**: Handle persistent tasks in the background.
3. **Popup/Options Scripts**: Manage the extension's UI interactions.

I extensively utilized the Chrome Extension API to ensure smooth integration of the different JavaScript runtimes. 

- **Persistence**: Search session data is stored using `chrome.storage.local`.
- **Inter-context Communication**: Handled via the `chrome.runtime` API, enabling ***message passing*** and ***port-based communication*** between content scripts, background scripts, and the popup.

This approach ensures a responsive and seamless user experience.


### Backend Architecture


#### Tools
The backend is built using **FastAPI** (Python), **Langchain** (RAG Framework), **Chroma** (vector database), **Elevenlabs** (txt-to-speech), **GroqCloud** (LLM Inference). 

#### Systems Overview
<img width="849" alt="Screenshot 2024-08-30 at 1 06 58 PM" src="https://github.com/user-attachments/assets/e57282d7-7084-4318-b3ec-0059f3d3261b">


#### Endpoints
Below is a quick summary of the key endpoints:

1. **GET `/api_keys`**: Returns the user's API keys.

2. **POST `/llm_call`**: Sends a request to the GroqCloud model to receive an LLM response.

3. **POST `/rag_call`**: 
   - Receives a webpage's content (context) and user query.
   - **Chunking**: Splits the context into smaller chunks.
   - **Vectorization & Storage**: Vectorizes the chunks using <a href="https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2" target="_blank"> huggingface embeddings model</a> and stores them in Chroma DB.
   - **Query Matching**: Vectorizes the query and retrieves the top `n` most relevant chunks using cosine similarity.
   - **Prompt Construction**: Combines the query with the relevant chunks into a template prompt.
   - **LLM Call**: Forwards the prompt to the `/llm_call` endpoint.
   - **Response**: The output is returned as the final response.
4. **POST `/text_to_speech_call`**: Sends a request to the ElevenLabs model to generate an audio file, which is then played. However, there's significant delay before the audio begins to play.
5. **WebSocket `/text_to_speech_websocket`**: Establishes a WebSocket connection between the ElevenLabs API and the Chrome extension client. As audio data is streamed from the API to the local backend, it is forwarded to the frontend, where it is queued and played using the WebAudio API. Once all audio buffers are played, the WebSocket connection is closed.
6. **POST `/pass-api-keys`**: Accepts API keys for GroqCloud and ElevenLabs, validates them by making test requests, and if successful, stores them in the backend.


## Installation (need to update!!!)

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/fastr.git
    ```
2. Navigate to the project directory:
    ```bash
    cd fastr
    ```
3. Install dependencies:
    ```bash
    npm install
    ```
4. Load the extension into Chrome:
    1. Open Chrome and go to `chrome://extensions/`.
    2. Enable "Developer mode" (toggle in the top right corner).
    3. Click "Load unpacked" and select the `fastr` project directory.

## Usage

1. Navigate to any webpage in Chrome.
2. Highlight the text you want to query.
3. Press the `Tab` key to open the Fastr chatbox.
4. Interact with the LLM to get context-aware insights and information.
5. **Save Responses**: Responses are saved automatically between sessions, allowing you to revisit your questions and answers later.
6. **Export to TXT**: At any time, export the entire session (questions and responses) to a `.txt` file for easy documentation.

## Contributing

Contributions are welcome! To contribute to **Fastr**, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, feel free to reach out via [pruthvi.innamuri@berkeley.edu](mailto:pruthvi.innamuri@berkeley.edu).

