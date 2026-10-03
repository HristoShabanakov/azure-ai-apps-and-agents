# Flux Image Generation Agent

A simple Python image-generation application built with Microsoft Foundry and the FLUX.2 [flex] model from Black Forest Labs.

The application accepts text prompts, sends them to an Azure-hosted FLUX model, and saves the generated image locally.

## Features

- Generate images from natural-language prompts
- Enter multiple prompts without restarting the application
- Save generated images automatically as PNG files
- Support Base64 and URL-based image responses
- Store configuration in environment variables

## Requirements

- Python 3.11+
- Azure subscription
- Microsoft Foundry resource
- FLUX.2 [flex] deployment
- `requests`
- `python-dotenv`

## Setup

Create a virtual environment:

```cmd
python -m venv .venv
```

Activate it in Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Install the dependencies:

```cmd
python -m pip install requests python-dotenv
```

## Environment Variables

Create a `.env` file:

```env
AZURE_IMAGE_ENDPOINT=https://your-resource.services.ai.azure.com/providers/blackforestlabs/v1/flux-2-flex?api-version=preview
AZURE_API_KEY=your-api-key
IMAGE_MODEL=FLUX.2-flex
```

Do not commit the real `.env` file or your Azure API key to GitHub.

Your `.env.example` can contain the same variable names with placeholder values.

## Run

```cmd
python flux_image_agent.py
```

Example:

```text
Flux Image Generation Agent
Describe the image you want to generate.
Type 'exit' or 'quit' to stop.

Prompt: A photograph of a red fox in an autumn forest

Generating image...

Image saved to: generated_image_20261003_110500.png
```

Enter another prompt to generate another image, or type `exit` / `quit` to stop.

## How It Works

```text
Text prompt
   ↓
Python application
   ↓
Microsoft Foundry
   ↓
FLUX.2 [flex]
   ↓
Base64 image or image URL
   ↓
PNG file saved locally
```

## Project Structure

```text
flux-image-generation-agent/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── flux_image_agent.py
```

## Recommended `.gitignore`

```gitignore
.venv/
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.vscode/
.DS_Store
Thumbs.db
```

## Learning Context

This project is part of a larger repository created while learning how to build AI workloads and applications with Microsoft Foundry.

## License

See the root repository `LICENSE` file for licensing information.
