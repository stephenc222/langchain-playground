#!/usr/bin/env python3

from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)

text = "What would be a good company name for a company that makes colorful socks?"
answer = llm(text)
print(answer.strip())

