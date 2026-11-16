def calculate_token_usage(first_usage, second_usage):
    total_input_tokens = (
        first_usage.prompt_token_count +
        second_usage.prompt_token_count
    )

    total_output_tokens = (
        first_usage.candidates_token_count +
        second_usage.candidates_token_count
    )

    total_tokens = total_input_tokens + total_output_tokens

    return {
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_tokens
    }

def count_conversation_tokens(client, model, conversation_history, system_instruction):
    history_response = client.models.count_tokens(
        model=model,
        contents=conversation_history
    )

    instruction_response = client.models.count_tokens(
        model=model,
        contents=system_instruction
    )

    total_tokens = (
        history_response.total_tokens +
        instruction_response.total_tokens
    )

    return total_tokens

def manage_conversation_history(client, model, conversation_history, system_instruction, max_input_tokens):
    while True:
        total_tokens = count_conversation_tokens(
            client,
            model,
            conversation_history,
            system_instruction
        )

        if total_tokens <= max_input_tokens:
            return total_tokens

        if len(conversation_history) > 1:
            del conversation_history[:2]
            print("Removed oldest conversation exchange.")
        else:
            raise ValueError(
                "The current request exceeds the input token budget."
            )