import json
import os
from pathlib import Path

from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisResult
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


load_dotenv()

endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
key = os.getenv("CONTENTUNDERSTANDING_KEY", "").strip()

analyzer_id = os.getenv(
    "CONTENTUNDERSTANDING_ANALYZER_ID",
    "prebuilt-documentFields",
)

api_version = os.getenv(
    "CONTENTUNDERSTANDING_API_VERSION",
    "2026-06-01-preview",
)


def create_client() -> ContentUnderstandingClient:
    """Create and return an authenticated Content Understanding client."""

    credential = (
        AzureKeyCredential(key)
        if key
        else DefaultAzureCredential()
    )

    return ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version,
    )


def analyze_file(
    client: ContentUnderstandingClient,
    file_path: str,
) -> AnalysisResult:
    """
    Analyze a local file using Azure AI Content Understanding.

    Args:
        client: Authenticated Content Understanding client.
        file_path: Path to the local file.

    Returns:
        The analysis result returned by Azure.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    print(f"\nAnalyzing with {analyzer_id}...")
    print(f"File: {path}\n")

    with path.open("rb") as file:
        file_bytes = file.read()

    poller = client.begin_analyze_binary(
        analyzer_id=analyzer_id,
        binary_input=file_bytes,
    )

    return poller.result()


def display_result(result: AnalysisResult) -> None:
    """Display the analysis result as formatted JSON."""

    print("=" * 50)
    print("Analysis result:")
    print("=" * 50)
    print()

    result_json = json.dumps(
        result.as_dict(),
        indent=2,
    )

    print(result_json)


def run_agent() -> None:
    """Run an interactive local-file analysis session."""

    client = create_client()

    print("\nContent Understanding Agent")
    print("Enter the path of a local file to analyze.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        file_path = input("File path: ").strip().strip('"')

        if file_path.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not file_path:
            continue

        try:
            result = analyze_file(
                client=client,
                file_path=file_path,
            )

            display_result(result)

        except FileNotFoundError as error:
            print(f"\n[File Error]: {error}\n")

        except AzureError as error:
            print(f"\n[Azure Error]: {error}\n")

        except Exception as error:
            print(f"\n[Unexpected Error]: {error}\n")


if __name__ == "__main__":
    run_agent()