
import os
from datetime import datetime

from google import genai
from dotenv import load_dotenv

from prompts import SYSTEM_INSTRUCTION, RESPONSE_INSTRUCTION
from schemas import AssistantResponse
from task_manager import create_task, update_task, delete_task, complete_task, get_all_tasks, delete_all_tasks, complete_all_tasks
from utils import calculate_token_usage

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

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=conversation_history,
        config={
            "system_instruction": system_instruction,
            "response_mime_type": "application/json",
            "response_schema": AssistantResponse,
        }
    )

    first_usage = response.usage_metadata
  
    assistant_data = AssistantResponse.model_validate_json(
        response.text
    )

    if assistant_data.action == "create_task":
        result = create_task(assistant_data.task)

    elif assistant_data.action == "list_tasks":
        if assistant_data.filters:
            result = get_all_tasks(
                **assistant_data.filters.model_dump(
                    exclude_none=True
                )
            )
        else:
            result = get_all_tasks()

    elif assistant_data.action == "update_task":
        result = update_task(assistant_data.task_update)

    elif assistant_data.action == "delete_task":
        result = delete_task(assistant_data.task.title)

    elif assistant_data.action == "complete_task":
        result = complete_task(assistant_data.task.title)
    
    elif assistant_data.action == "complete_all_tasks":
        result = complete_all_tasks()

    elif assistant_data.action == "delete_all_tasks" and assistant_data.confirmation == "confirmed":
        result = delete_all_tasks(confirmed=True)

    else:
        result = assistant_data.message

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
    response = client.models.generate_content_stream(
        model="gemini-3.5-flash-lite",
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