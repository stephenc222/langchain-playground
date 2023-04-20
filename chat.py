#!/usr/bin/env python3

import openai
import os
import sys
import datetime
from sliding_context_window import SlidingContextWindow

# NOTE: For a more "normal" ChatGPT type of interaction.

MAX_TOKENS = 1500
COMPLETION_TOKENS = 2500
MODEL = "gpt-3.5-turbo"

# Set up OpenAI API key and chat log filename
openai.api_key = os.environ["OPENAI_API_KEY"]
start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H')
chat_log_filename = f"{start_timestamp}_chat_log.txt"

chat_log_dir = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'logs/chat_logs')

# Create chat_logs directory if it doesn't exist
if not os.path.exists(chat_log_dir):
    os.makedirs(chat_log_dir)


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


def main():
    chat_log = ""
    context_window = SlidingContextWindow(MAX_TOKENS, MODEL)
    try:
        while True:
            user_input = input("> ")
            if user_input == "quit":
                break
            context_window.add_message("user", f"User: {user_input}\nAI:")
            response = get_response(context_window.get_context())
            context_window.add_message("assistant", response.content)
            if response.content == "":
                print("Sorry, I didn't understand what you said.")
            elif response.content == "[STOP]":
                print("AI: Goodbye!")
                break
            else:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                chat_log += f"{timestamp}: User: {user_input}\n"
                chat_log += f"{timestamp}: AI: {response.content}\n"
                print(f"AI: {response.content}")
    except KeyboardInterrupt or Exception:
        with open(os.path.join(chat_log_dir, chat_log_filename), "a") as f:
            f.write(chat_log)
        sys.exit(1)

    with open(os.path.join(chat_log_dir, chat_log_filename), "a") as f:
        f.write(chat_log)


if __name__ == "__main__":
    main()
