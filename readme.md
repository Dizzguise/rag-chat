# RAG-Chat

RAG-Chat is a powerful chatbot built using the LangChain library. It can decide whether to respond using preloaded document data or perform a real-time web search using the Brave Search API. This flexibility allows it to provide accurate and up-to-date information based on the user's queries.

## Features

- **Document Loading**: Load documents from specified files, directories, or predefined paths.
- **Decision Making**: Uses the Ollama LLM to decide if a query can be answered using preloaded documents or if a web search is required.
- **Web Search**: Integrates with the Brave Search API to fetch real-time information when necessary.
- **Context Management**: Efficiently manages context for accurate and relevant responses.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/rag-chat.git
    cd rag-chat
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. **API Keys**: Ensure you have your Brave Search API key.

2. **Configuration File**: Edit the `config.yaml` file to include your API keys and other settings.
    ```yaml
    logging:
      level: DEBUG

    llm:
      model: llama3

    web_search:
      api_key: YOUR_BRAVE_SEARCH_API_KEY
      count: 10
      extra_snippets: true
    ```

## Usage

1. **Run the chatbot**:
    ```sh
    python main.py
    ```

2. **Interact with the chatbot**:
    - Upon starting, you will be prompted to choose a document loading method.
    - Type your queries and receive responses based on preloaded documents or real-time web search results.
    - Type `exit` or `quit` to end the session.

## File Structure

- **main.py**: The entry point of the application. Handles user input and coordinates the decision-making and response generation.
- **config.yaml**: Configuration file for API keys and settings.
- **document_loader.py**: Handles loading documents from specified files or directories.
- **retrieval_chain.py**: Creates the retrieval chain for document-based responses.
- **decision_agent.py**: Decides whether to use document data or perform a web search.
- **query_agent.py**: Handles querying the document vector store.
- **context_agent.py**: Manages context for generating responses.
- **web_search.py**: Integrates with the Brave Search API to perform web searches.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Contact

For any questions or feedback, please open an issue on GitHub.

---

Thank you for using RAG-Chat! We hope it provides valuable assistance in your projects.
