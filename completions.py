#!/usr/bin/env python3

from dotenv import load_dotenv
import openai
import os
import sys
import datetime

load_dotenv()

# NOTE: For more unusual and somewhat non-sensical output.

# Set up OpenAI API key and completion log filename
openai.api_key = os.environ["OPENAI_API_KEY"]
start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
completion_log_filename = f"{start_timestamp}_completion_log.txt"

# Create completion-logs directory if it doesn't exist
if not os.path.exists("completion-logs"):
    os.makedirs("completion-logs")

def get_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop="\nUser:",
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def main():
    completion_log = ""
    try:
        while True:
            user_input = input("> ")
            if user_input == "quit":
                break
            prompt = f"User: {user_input}\nAI:"
            response = get_response(prompt)
            if response == "":
                print("Sorry, I didn't understand what you said.")
            elif response == "[STOP]":
                print("AI: Goodbye!")
                break
            else:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                completion_log += f"{timestamp}: User: {user_input}\n"
                completion_log += f"{timestamp}: AI: {response}\n"
                print(f"AI: {response}")
    except KeyboardInterrupt:
        with open(os.path.join("completion-logs", completion_log_filename), "a") as f:
            f.write(completion_log)
        sys.exit(1)

    with open(os.path.join("completions-logs", completion_log_filename), "a") as f:
        f.write(completion_log)

if __name__ == "__main__":
    main()
