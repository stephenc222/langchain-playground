#!/usr/bin/env python3


import tiktoken
import openai
import os
import sys
import datetime

# NOTE: For a more "normal" ChatGPT type of interaction.

MAX_TOKENS = 1500
COMPLETION_TOKENS = 2500
MODEL = "gpt-3.5-turbo"


encoding = tiktoken.encoding_for_model(MODEL)
# Set up OpenAI API key and chat log filename
openai.api_key = os.environ["OPENAI_API_KEY"]
start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H')
chat_log_filename = f"{start_timestamp}_chat_log.txt"

# Create chat_logs directory if it doesn't exist
if not os.path.exists("logs/chat_logs"):
    os.makedirs("logs/chat_logs")


def get_response(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        max_tokens=COMPLETION_TOKENS,
        n=1,
        stop="\nUser:",
        temperature=0.7,
    )
    return response.choices[0].message


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens


def truncate_messages(messages, chat_log, property, target_sum):
    current_sum = 0
    truncated_messages = []
    next_chat_log = chat_log

    # Loop over the array and sum the "num" property of each dict
    for message in reversed(messages):
        current_sum += num_tokens_from_string(message[property])

        # If the sum reaches the target value, break out of the loop and flush the chat_log
        if current_sum >= target_sum:
            with open(os.path.join("logs/chat_logs", chat_log_filename), "a") as f:
                f.write(chat_log)
                next_chat_log = ''
            break
        truncated_messages.insert(0, message)

    # Slice the array to remove the first "num_items" items
    return truncated_messages, next_chat_log


def main():
    chat_log = ""
    chat_messages = []
    try:
        while True:
            user_input = input("> ")
            if user_input == "quit":
                break
            prompt = f"User: {user_input}\nAI:"
            chat_messages.append({
                "role": "user",
                "content": prompt
            })
            response = get_response(chat_messages)
            chat_messages.append(response)
            chat_messages, chat_log = truncate_messages(
                chat_messages, chat_log, 'content', MAX_TOKENS)
            if response == "":
                print("Sorry, I didn't understand what you said.")
            elif response == "[STOP]":
                print("AI: Goodbye!")
                break
            else:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                chat_log += f"{timestamp}: User: {user_input}\n"
                chat_log += f"{timestamp}: AI: {response.content}\n"
                print(f"AI: {response.content}")
    except KeyboardInterrupt or Exception:
        with open(os.path.join("logs/chat_logs", chat_log_filename), "a") as f:
            f.write(chat_log)
        sys.exit(1)

    with open(os.path.join("logs/chat_logs", chat_log_filename), "a") as f:
        f.write(chat_log)


if __name__ == "__main__":
    main()
