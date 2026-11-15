from assistant import chat_with_assistant


while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break

    print("Assistant: ", end="", flush=True)

    chat_with_assistant(user_input)