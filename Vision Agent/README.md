# Vision Agent

A simple Python computer vision application built with Microsoft Foundry and the OpenAI Responses API.

The app lets you load a local image, ask questions about it, and continue the conversation with follow-up questions without restarting the script.

## Features

- Analyze local images with a vision-capable model
- Ask multiple follow-up questions about the same image
- Preserve conversation context with `previous_response_id`
- Authenticate with Azure using `DefaultAzureCredential`
- Store configuration in environment variables
- Convert local images to Base64 data URLs automatically

## Requirements

- Python 3.11+
- Azure subscription
- Microsoft Foundry project
- A deployed vision-capable model
- Azure CLI

## Setup

Create and activate a virtual environment.

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Install the dependencies:

```cmd
python -m pip install openai azure-identity python-dotenv
```

Authenticate with Azure:

```cmd
az login
```

## Environment Variables

Create a `.env` file in the project folder:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.services.ai.azure.com/openai/v1
VISION_MODEL=your-model-deployment-name
```

Do not commit your `.env` file to GitHub.

You can also create a `.env.example` file with placeholder values:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.services.ai.azure.com/openai/v1
VISION_MODEL=your-model-deployment-name
```

## Run

Start the application with:

```cmd
python vision_agent.py
```

Enter the path to a local image when prompted:

```text
Image path: C:\Users\YourName\Pictures\example.jpg
```

Then ask questions such as:

```text
You: Describe this image.
You: How many people are visible?
You: What objects are on the table?
You: Is there any text in the image?
```

Type `exit` or `quit` to stop the conversation.

## How It Works

```text
Local image
   ↓
Base64 encoding
   ↓
Microsoft Foundry / OpenAI Responses API
   ↓
Vision model
   ↓
Conversational response
```

The image is sent with the first question. Follow-up questions use the previous response ID so the conversation can continue without resending the image each time.

## Project Structure

```text
Vision Agent/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── vision_agent.py
```

## Recommended `.gitignore`

```gitignore
.venv/
.env
__pycache__/
*.py[cod]
.vscode/
.DS_Store
Thumbs.db
```

## Learning Context

This project was created while learning how to build AI workloads and applications with Microsoft Foundry, including computer vision and multimodal AI.

## License

This project is intended for learning and experimentation. If the repository uses the MIT License, see the root `LICENSE` file for details.
