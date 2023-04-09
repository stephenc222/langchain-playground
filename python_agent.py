#!/usr/bin/env python3

from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.llms.openai import OpenAI

# Neat example of creating a neural network with LangChain, inspired by the docs example:
# https://python.langchain.com/en/latest/modules/agents/toolkits/examples/python.html

agent_executor = create_python_agent(
    llm=OpenAI(temperature=0, max_tokens=1000),
    tool=PythonREPLTool(),
    verbose=True
)

agent_executor.run("""Create a single neuron neural network in PyTorch.
Take training data for y=3x + 1. Train for 1000 epochs and print every 100 epochs.
Return prediction for x = 6""")