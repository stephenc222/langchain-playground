import openai
import os
import sys
import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from sliding_context_window import SlidingContextWindow

# NOTE: For a more "normal" ChatGPT type of interaction.
# TODO: make this full screen, syntax highlighting, easier to paste in chunks of code

MAX_TOKENS = 1500
COMPLETION_TOKENS = 2500
MODEL = "gpt-3.5-turbo"

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


class ChatPrompt:
    def __init__(self, execute_fn, style_dict=None):
        self.execute_fn = execute_fn
        self.style = Style.from_dict(style_dict or {})
        self.session = PromptSession(style=self.style)

    def start(self):
        chat_log = ""
        context_window = SlidingContextWindow(MAX_TOKENS, MODEL)
        try:
            while True:
                text = self.session.prompt(message='> ')
                if text == "quit":
                    break
                context_window.add_message("user", f"User: {text}\nAI:")
                response = self.execute_fn(context_window.get_context())
                context_window.add_message("assistant", response.content)
                if response.content == "":
                    print("Sorry, I didn't understand what you said.")
                elif response.content == "[STOP]":
                    print("AI: Goodbye!")
                    break
                else:
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    chat_log += f"{timestamp}: User: {text}\n"
                    chat_log += f"{timestamp}: AI: {response.content}\n"
                    print(f"AI: {response.content}")
        except KeyboardInterrupt or Exception:
            with open(os.path.join("logs/chat_logs", chat_log_filename), "a") as f:
                f.write(chat_log)
            sys.exit(1)

        with open(os.path.join("logs/chat_logs", chat_log_filename), "a") as f:
            f.write(chat_log)


# Usage
if __name__ == "__main__":
    chat_prompt = ChatPrompt(execute_fn=get_response)
    chat_prompt.start()
