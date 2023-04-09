#!/usr/bin/env python3

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI


# https://python.langchain.com/en/latest/modules/agents/tools/getting_started.html
llm = OpenAI(temperature=0)

tools = load_tools(["terminal"], llm=llm)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("What is the local system time? Format it month/date/year with time.")