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