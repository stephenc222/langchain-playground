from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

load_dotenv()

llm = OpenAI(temperature=0.9)

text = "What would be a good company name for a company that makes colorful socks?"
answer = llm(text)
print(answer.strip())

