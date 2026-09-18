# Before running the sample:
#    pip install azure-ai-projects>=2.1.0
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
speech_key = os.environ["SPEECH_KEY"]
speech_region = os.environ["SPEECH_REGION"]

stt_endpoint = f"https://{speech_region}.stt.speech.microsoft.com"
tts_endpoint = f"https://{speech_region}.tts.speech.microsoft.com"

my_agent = os.environ["AGENT_NAME"]
my_version = os.environ["AGENT_VERSION"]

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

project_client = AIProjectClient(endpoint=endpoint,credential=DefaultAzureCredential(),)

openai_client = project_client.get_openai_client()

# ---------------------------
# Azure Speech Recognition
# ---------------------------

speech_key = os.environ["SPEECH_KEY"]

# Speech-to-text configuration
stt_config = speechsdk.SpeechConfig(subscription=speech_key,endpoint=stt_endpoint)
    
stt_config.speech_recognition_language = "en-US"

microphone_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=stt_config,audio_config=microphone_config)
    

# ---------------------------
# Azure Text-to-Speech
# ---------------------------

tts_config = speechsdk.SpeechConfig(subscription=speech_key,endpoint=tts_endpoint)
    
speaker_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=tts_config,audio_config=speaker_config)

# ---------------------------
# Conversation
# ---------------------------

messages = []


def run_conversation():

    print("Speech Agent is ready.")
    print("Press ENTER and speak.")
    print("Say 'exit' or 'quit' to stop.\n")

    while True:

        input("Press ENTER to speak...")

        print("Listening...")

        result = speech_recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:

            user_input = result.text.strip()

            print(f"\nYou: {user_input}")

            if user_input.lower().rstrip(".") in ("exit", "quit"):
                print("Goodbye!")
                break

            messages.append({
                "role": "user",
                "content": user_input
            })

            try:
                response = openai_client.responses.create(
                    input=messages,
                    extra_body={
                        "agent_reference": {
                            "name": my_agent,
                            "version": my_version,
                            "type": "agent_reference"
                        }
                    }
                )

                answer = response.output_text

                print(f"\nAgent: {answer}\n")

                # Speak the answer
                synthesis_result = (
                    speech_synthesizer
                    .speak_text_async(answer)
                    .get()
                )

                if synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    print("Audio played successfully.\n")

                elif synthesis_result.reason == speechsdk.ResultReason.Canceled:
                    cancellation = synthesis_result.cancellation_details

                    print("Speech synthesis canceled.")

                    if cancellation.error_details:
                        print("Error:", cancellation.error_details)

                # Remember agent response
                messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                print(f"\nAgent error: {e}\n")


        elif result.reason == speechsdk.ResultReason.NoMatch:

            print("\nI couldn't understand what you said.\n")


        elif result.reason == speechsdk.ResultReason.Canceled:

            cancellation = result.cancellation_details

            print("\nSpeech recognition canceled.")

            if cancellation.error_details:
                print("Error:", cancellation.error_details)


run_conversation()