# Oryza Chatbot

Oryza Chatbot is a lightweight AI assistant that runs locally through Ollama and serves a clean web interface for chatting with a local model. It is designed for privacy-friendly, self-hosted use and can be deployed with Docker.

## Features

- Local AI chat using Ollama
- Oryza-branded web interface
- Fast response generation
- Privacy-focused deployment on your own machine
- Simple Flask-based chat UI
- Docker-ready setup with Nginx reverse proxy

## Tech Stack

- Python
- Flask
- Ollama
- HTML/CSS/JavaScript
- Docker / Docker Compose

## Prerequisites

Before running the project, ensure you have:

- Python 3.10+
- Docker and Docker Compose
- Ollama installed
- A local model pulled, for example:

```bash
ollama pull qwen2.5:1.5b
```

## Local Development

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app locally:

```bash
python app/main.py
```

Open your browser at:

```text
http://localhost:5000
```

## Docker Deployment

From the project root, run:

```bash
docker compose up -d --build
```

The app will be served through the proxy on:

```text
http://localhost/
```

For a custom domain, update the Nginx host configuration in `nginx.conf` and point your DNS to the server IP.

## Project Structure

```text
Qwen-Chat/
├── app/
│   └── main.py
├── templates/
│   └── index.html
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── requirements.txt
└── README.md
```

## How It Works

1. The Flask app receives the user prompt.
2. It sends the prompt to Ollama.
3. Ollama runs the selected local model.
4. The generated response is returned to the web UI.

## Future Improvements

- Conversation history
- Streaming responses
- Multiple model selection
- Dark mode
- Authentication
- HTTPS with Let’s Encrypt

## License

This project is licensed under the MIT License.

## Author

Oryza Labs - Rushikesh Mohalkar
