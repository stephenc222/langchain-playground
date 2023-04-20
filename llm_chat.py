#!/usr/bin/env python3

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.utilities import BashProcess
from langchain.chat_models import ChatOpenAI
from tiktoken import get_encoding
import os
import sys
import datetime
from sliding_context_window import SlidingContextWindow

# Constants
MAX_TOKENS = 1500
MODEL = "gpt-3.5-turbo"
ENCODING = "cl100k_base"

start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H')
chat_log_filename = f"{start_timestamp}_llm_chat_log.txt"

# Create llm_chat_logs directory if it doesn't exist
chat_log_dir = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'logs/llm_chat_logs')

# Create chat_logs directory if it doesn't exist
if not os.path.exists(chat_log_dir):
    os.makedirs(chat_log_dir)


bash = BashProcess()

# Initialize SlidingContextWindow
context_window = SlidingContextWindow(MAX_TOKENS, MODEL)
context_window.encoding = get_encoding(ENCODING)

llm = ChatOpenAI(temperature=0)

search = SerpAPIWrapper()

tools = [
    Tool(
        name="Bash Commands",
        func=bash.run,
        description="useful for running bash commands inside a unix terminal"
    ),
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    )
]

agent_chain = initialize_agent(
    tools, llm, agent="chat-conversational-react-description", verbose=True)


def main():
    chat_log = ""
    message_timestamps = []
    try:
        while True:
            user_input = input("> ")
            if user_input == "quit":
                break
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message_timestamps.append(timestamp)
            prompt = user_input.strip("> ")
            context_window.add_message("user", prompt)

            # Include 'chat_history' key in the inputs
            inputs = {
                'input': prompt,
                'chat_history': context_window.get_langchain_context()
            }

            response = agent_chain.run(inputs)
            context_window.add_message("assistant", response)
            message_timestamps.append(timestamp)
            print('AI:', response)

    except KeyboardInterrupt:
        with open(os.path.join(chat_log_dir, chat_log_filename), "a") as f:
            idx = 0
            for message in context_window.get_context():
                chat_log += f"{message_timestamps[idx]}: {message['role']}: {message['content']}\n"
                idx += 1
            f.write(chat_log)
        sys.exit(1)

    with open(os.path.join(chat_log_dir, chat_log_filename), "a") as f:
        idx = 0
        for message in context_window.get_context():
            chat_log += f"{message_timestamps[idx]}: {message['role']}: {message['content']}\n"
            idx += 1
        f.write(chat_log)


if __name__ == "__main__":
    main()
