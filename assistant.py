
import os
from datetime import datetime

from google import genai
from google.genai import errors
from dotenv import load_dotenv

from prompts import SYSTEM_INSTRUCTION, RESPONSE_INSTRUCTION
from schemas import AssistantResponse
from utils import calculate_token_usage, count_conversation_tokens, manage_conversation_history
from config import MODEL_NAME, GENERATION_CONFIG
from pydantic import ValidationError

from handlers import execute_action

MAX_INPUT_TOKENS = 8000

load_dotenv()

api_key = os.getenv("GENAI_API_KEY")

client = genai.Client(api_key=api_key)

conversation_history = []

def chat_with_assistant(user_message):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    system_instruction = f"""
    {SYSTEM_INSTRUCTION}

    CURRENT DATE AND TIME:
    {current_datetime}

    Use this date and time when interpreting relative dates.

    Never assume the user has confirmed a destructive action.
    """

    conversation_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    history_tokens = manage_conversation_history(
        client,
        MODEL_NAME,
        conversation_history,
        system_instruction,
        MAX_INPUT_TOKENS
    )

    print(f"\nConversation history tokens: {history_tokens}")
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation_history,
            config={
                "system_instruction": system_instruction,
                "response_mime_type": "application/json",
                "response_schema": AssistantResponse,
            }
        )
    except errors.APIError as e:
        conversation_history.pop()
        print(f"\nGemini API error: {e}")
        print("I couldn't reach the API service. Please try again.")
        return

    first_usage = response.usage_metadata
  
    try:
        assistant_data = AssistantResponse.model_validate_json(response.text)
    except (ValidationError, ValueError, TypeError):
        conversation_history.pop()
        print("I couldn't process that response. Please try again.")
        return

    
    try:

        if assistant_data.action:
            result = execute_action(assistant_data)
        else:
            result = assistant_data.message

    except Exception as e:
        print(f"\nTask execution error: {e}")
        result = (
            "The task operation failed due to an internal application error. "
            "Do not claim it succeeded."
        )

    final_response, second_usage = generate_response(
        user_message,
        result
    )

    usage = calculate_token_usage(
        first_usage,
        second_usage
    )
    print("\n--- Combined Token Usage ---")
    print(f"Input tokens: {usage['input_tokens']}")
    print(f"Output tokens: {usage['output_tokens']}")
    print(f"Total tokens: {usage['total_tokens']}")

    conversation_history.append({
        "role": "model",
        "parts": [{"text": final_response}]
    })

    return final_response

def generate_response(user_message, action_result):
    try:
        response = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=[
                {
                    "role": "user",
                    "parts": [{
                        "text": f"""
                        USER REQUEST:
                        {user_message}

                        EXECUTION RESULT:
                        {action_result}

                        Generate a natural response to the user.
                        """
                    }]
                }
            ],
            config={
                "system_instruction": RESPONSE_INSTRUCTION
            }
        )
        full_response = ""
        usage= None
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text
            if chunk.usage_metadata:
                usage = chunk.usage_metadata
        print()
        return full_response, usage
    except errors.APIError as e:
        print(f"\nGemini streaming API error: {e}")
        print("I couldn't generate a response. Please try again.")
        return None, None