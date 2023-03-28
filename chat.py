#!/usr/bin/env python3

from dotenv import load_dotenv
import openai
import os
import sys
import datetime

# NOTE: For a more "normal" ChatGPT type of interaction.

load_dotenv()

# Set up OpenAI API key and chat log filename
openai.api_key = os.environ["OPENAI_API_KEY"]
start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
chat_log_filename = f"{start_timestamp}_chat_log.txt"

# Create chat-logs directory if it doesn't exist
if not os.path.exists("chat-logs"):
    os.makedirs("chat-logs")

def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        n=1,
        stop="\nUser:",
        temperature=0.7,
    )
    return response.choices[0].message

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
    except KeyboardInterrupt:
        with open(os.path.join("chat-logs", chat_log_filename), "a") as f:
            f.write(chat_log)
        sys.exit(1)

    with open(os.path.join("chat-logs", chat_log_filename), "a") as f:
        f.write(chat_log)

if __name__ == "__main__":
    main()
