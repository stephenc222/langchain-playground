#!/usr/bin/env python3

from dotenv import load_dotenv
from langchain import OpenAI, ConversationChain
import os

load_dotenv()

llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm, verbose=True)

print(conversation.predict(input="Hi there!"))
print(conversation.predict(input="I'm doing well! Just having a conversation with an AI."))


