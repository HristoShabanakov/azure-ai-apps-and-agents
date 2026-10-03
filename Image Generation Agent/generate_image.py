import base64
import os
from datetime import datetime

import requests
from dotenv import load_dotenv


# Load local configuration from .env.
load_dotenv()

# Keep environment-specific values outside the source code.
endpoint = os.environ["AZURE_IMAGE_ENDPOINT"]
api_key = os.environ["AZURE_API_KEY"]
model_name = os.environ["IMAGE_MODEL"]


def generate_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    guidance: float = 4.5,
    steps: int = 30,
) -> str:
    """
    Generate an image from a text prompt and save it locally.

    Args:
        prompt: Description of the image to generate.
        width: Width of the generated image in pixels.
        height: Height of the generated image in pixels.
        guidance: Controls how closely the model follows the prompt.
        steps: Number of inference steps used for generation.

    Returns:
        The path of the generated image file.
    """

    payload = {
        "model": model_name,
        "prompt": prompt,
        "width": width,
        "height": height,
        "output_format": "png",
        "guidance": guidance,
        "steps": steps,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print("\nGenerating image...")

    # Send the generation request to the Azure-hosted FLUX endpoint.
    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=120,
    )
    response.raise_for_status()

    result = response.json()

    # Use a timestamp to avoid overwriting earlier generated images.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"generated_image_{timestamp}.png"

    image_data = result["data"][0]

    # The API can return either Base64 image data or a downloadable URL.
    if "b64_json" in image_data:
        image_bytes = base64.b64decode(image_data["b64_json"])

        with open(output_path, "wb") as image_file:
            image_file.write(image_bytes)

    elif "url" in image_data:
        image_response = requests.get(image_data["url"], timeout=120)
        image_response.raise_for_status()

        with open(output_path, "wb") as image_file:
            image_file.write(image_response.content)

    else:
        raise ValueError("The API response did not contain image data.")

    return output_path


def run_agent() -> None:
    """
    Run an interactive image-generation session.

    The user can enter multiple prompts without restarting the script.
    Type 'exit' or 'quit' to stop the application.
    """

    print("\nFlux Image Generation Agent")
    print("Describe the image you want to generate.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        prompt = input("Prompt: ").strip()

        if prompt.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not prompt:
            continue

        try:
            output_path = generate_image(prompt)
            print(f"\nImage saved to: {output_path}\n")

        except requests.HTTPError as error:
            print(f"\nAPI error: {error}\n")

        except Exception as error:
            print(f"\nError: {error}\n")


# Run the application only when this file is executed directly.
if __name__ == "__main__":
    run_agent()
