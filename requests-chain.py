#!/usr/bin/env python3

from langchain.llms import OpenAI
from langchain.chains import LLMRequestsChain, LLMChain

from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

template = """Between >>> and <<< are the raw search result text from google.
Extract the answer to the question '{query}' or say "not found" if the information is not contained.
Use the format
Extracted:<answer or "not found">
>>> {requests_result} <<<
Extracted:"""

PROMPT = PromptTemplate(
    input_variables=["query", "requests_result"],
    template=template,
)

chain = LLMRequestsChain(llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=PROMPT))

question = "What are the Three (3) biggest countries, and their respective sizes?"
inputs = {
    "query": question,
    "url": "https://www.google.com/search?q=" + question.replace(" ", "+")
}

print(question)

print(chain(inputs)['output'].strip())

question = "Official 2022 US inflation rate"
inputs = {
    "query": question,
    "url": "https://www.google.com/search?q=" + question.replace(" ", "+")
}

print(question)

print(chain(inputs)['output'].strip())