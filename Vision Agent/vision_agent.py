import base64
import mimetypes
import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment_name = os.environ["VISION_MODEL"]

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default",
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)


def encode_image(image_path: str) -> str:
    """Convert a local image into a Base64 data URL."""

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        mime_type = "image/jpeg"

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:{mime_type};base64,{base64_image}"


def run_conversation(image_url: str) -> None:
    """
    Start an interactive conversation about an image.

    The image is included with the first request. Follow-up requests use
    the previous response ID to preserve the conversation context.

    Args:
        image_url: Base64-encoded image represented as a data URL.
    """

    previous_response_id = None
    first_question = True

    print("\nVision Agent is ready.")
    print("Ask questions about the image.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            if first_question:
                # The model needs the image only when starting the conversation.
                response = client.responses.create(
                    model=deployment_name,
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": question,
                                },
                                {
                                    "type": "input_image",
                                    "image_url": image_url,
                                },
                            ],
                        }
                    ],
                )

                first_question = False

            else:
                # Continue the same conversation without resending the image.
                response = client.responses.create(
                    model=deployment_name,
                    previous_response_id=previous_response_id,
                    input=question,
                )

            previous_response_id = response.id

            print(f"\nAgent: {response.output_text}\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    image_path = input("Image path: ").strip('"')
    image_url = encode_image(image_path)

    run_conversation(image_url)