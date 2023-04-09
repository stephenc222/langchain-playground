#!/usr/bin/env python3


from langchain.chains import APIChain
from langchain.chains.api import open_meteo_docs
from langchain.llms import OpenAI



llm = OpenAI(temperature=0)
chain_new = APIChain.from_llm_and_api_docs(llm, open_meteo_docs.OPEN_METEO_DOCS, verbose=True)


chain_new.run('What is the weather like right now in Austin, Texas, USA in degrees Farenheit?')