# Speech Agent

A simple Python voice assistant built with Azure AI Foundry and Azure Speech Services.

The application listens through the microphone, converts speech to text, sends the message to an Azure AI Foundry agent, and reads the agent's response aloud.

## Features

- Speech-to-text using Azure Speech
- Azure AI Foundry agent integration
- Text-to-speech responses
- Conversation history for follow-up questions
- Configuration through environment variables

## Requirements

- Python 3.11+
- Azure subscription
- Azure AI Foundry project and agent
- Azure Speech access
- Azure CLI

## Setup

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Authenticate with Azure:

```bash
az login
```

## Environment Variables

Create a `.env` file in the project root:

```env
FOUNDRY_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project

SPEECH_KEY=your-speech-key
SPEECH_REGION=your-region

AGENT_NAME=your-agent-name
AGENT_VERSION=your-agent-version
```

Do not commit your `.env` file or any Azure keys to GitHub.

## Run

```bash
python text_agent.py
```

Press **Enter**, speak into your microphone, and wait for the agent to respond.

Say `exit` or `quit` to stop the application.

## Project Flow

```text
Microphone
   ↓
Azure Speech-to-Text
   ↓
Azure AI Foundry Agent
   ↓
Azure Text-to-Speech
   ↓
Speakers
```

## Security

Secrets and environment-specific configuration should be stored in `.env`.

Make sure `.env` and `.venv` are included in `.gitignore`.

## License

This project is intended for learning and experimentation.
