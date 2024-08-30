# Fastr

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

[![Fastr Demo]


https://github.com/user-attachments/assets/c524ef86-cd62-42cb-9f6e-7374eed60dae


## Systems Architecture

Below is an overview of the system architecture that powers Fastr:

![Fastr Systems Architecture](diagrams/architecture-diagram-link-here)

## Installation

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

For any inquiries or feedback, feel free to reach out via [your-email@example.com](mailto:your-email@example.com).

