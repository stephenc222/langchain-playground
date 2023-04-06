#!/usr/bin/env python3

from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

db = SQLDatabase.from_uri("sqlite:///./chinook.db")
llm = OpenAI(temperature=0)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

db_chain.run("How many employees are there?")


_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If someone asks for the table foobar, they really mean the employee table.

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

db_chain = SQLDatabaseChain(llm=llm, database=db, prompt=PROMPT, verbose=True)

db_chain.run("How many employees are there in the foobar table?")


db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, top_k=3)

db_chain.run("What are some example tracks by composer Johann Sebastian Bach?")