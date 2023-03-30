#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.utilities import BashProcess
from langchain.chat_models import ChatOpenAI
import os
import sys
import datetime

load_dotenv()

start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
chat_log_filename = f"{start_timestamp}_llm_chat_log.txt"

# Create llm-chat-logs directory if it doesn't exist
if not os.path.exists("logs/llm-chat-logs"):
    os.makedirs("logs/llm-chat-logs")

bash = BashProcess()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm=ChatOpenAI(temperature=0)

search = SerpAPIWrapper()

tools = [
    Tool(
        name = "Bash Commands",
        func=bash.run,
        description="useful for running bash commands inside a unix terminal"
    ),
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    )
]

agent_chain = initialize_agent(tools, llm, agent="chat-conversational-react-description", verbose=True, memory=memory)

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
            agent_chain.run(input=prompt)
            message_timestamps.append(timestamp)
    except KeyboardInterrupt:
        with open(os.path.join("logs/llm-chat-logs", chat_log_filename), "a") as f:
            idx = 0
            for message in agent_chain.memory.chat_memory.messages:
                chat_log += f"{message_timestamps[idx]}: {message.type}: {message.content}\n"
                idx += 1
 
            f.write(chat_log)

        sys.exit(1)

    with open(os.path.join("logs/llm-chat-logs", chat_log_filename), "a") as f:
        idx = 0
        for message in agent_chain.memory.chat_memory.messages:
            chat_log += f"{message_timestamps[idx]}: {message.type}: {message.content}\n"
            idx += 1

        f.write(chat_log)

if __name__ == "__main__":
    main()


