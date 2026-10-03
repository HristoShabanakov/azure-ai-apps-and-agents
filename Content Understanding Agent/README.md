# Content Understanding Agent

A simple Python application built with Azure AI Content Understanding.

The application analyzes local files from your computer using a prebuilt Content Understanding analyzer and displays the extracted results as formatted JSON.

## Features

- Analyze local files directly from your PC
- Use Azure AI Content Understanding
- Support interactive analysis without restarting the script
- Authenticate with either Azure API key or `DefaultAzureCredential`
- Configure endpoint, analyzer, and API version through environment variables
- Display structured analysis results as JSON

## Requirements

- Python 3.9+
- Azure subscription
- Microsoft Foundry resource with Content Understanding enabled
- Azure CLI if using `DefaultAzureCredential`

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
python -m pip install --pre azure-ai-contentunderstanding
python -m pip install azure-identity python-dotenv
```

If you are using `DefaultAzureCredential`, authenticate with Azure:

```cmd
az login
```

## Environment Variables

Create a `.env` file in the project folder:

```env
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=
CONTENTUNDERSTANDING_ANALYZER_ID=prebuilt-documentFields
CONTENTUNDERSTANDING_API_VERSION=2026-06-01-preview
```

If `CONTENTUNDERSTANDING_KEY` is left empty, the application uses `DefaultAzureCredential`.

Do not commit your real `.env` file to GitHub.

A safe `.env.example` can contain:

```env
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=
CONTENTUNDERSTANDING_ANALYZER_ID=prebuilt-documentFields
CONTENTUNDERSTANDING_API_VERSION=2026-06-01-preview
```

## Run

Start the application with:

```cmd
python content_understanding_agent.py
```

Enter the path to a local file when prompted:

```text
Content Understanding Agent
Enter the path of a local file to analyze.
Type 'exit' or 'quit' to stop.

File path: C:\Users\YourName\Documents\invoice.pdf
```

The application will analyze the file and print the result as formatted JSON.

You can enter another file path immediately without restarting the script.

Type `exit` or `quit` to stop the application.

## How It Works

```text
Local file
   ↓
Python application
   ↓
Azure AI Content Understanding
   ↓
Prebuilt analyzer
   ↓
Structured analysis result
   ↓
Formatted JSON output
```

## Project Structure

```text
content-understanding-agent/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── content_understanding_agent.py
```

## Requirements File

A simple `requirements.txt` can contain:

```text
azure-ai-contentunderstanding
azure-identity
python-dotenv
```

Because the Content Understanding SDK is currently installed as a pre-release package, install it with:

```cmd
python -m pip install --pre azure-ai-contentunderstanding
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
