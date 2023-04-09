#!/usr/bin/env python3

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredFileLoader
from langchain.indexes import VectorstoreIndexCreator
import nltk
import ssl

# NOTE: resolves an issue with ssl for nltk downloads
# https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

space_loader = UnstructuredFileLoader("./example_space.html")
state_of_the_union_loader = UnstructuredFileLoader("./example_state_of_the_union.html")

space_docs = space_loader.load()
state_of_the_union_docs = state_of_the_union_loader.load()

index = VectorstoreIndexCreator(
    vectorstore_cls=Chroma,
    embedding=OpenAIEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
).from_loaders([space_loader, state_of_the_union_loader])

query = "What is in every Country?"
print('query: ', query)
answer = index.query(query)
print('answer: ',answer.strip())

query = "What is SpaceX doing?"
answer = index.query(query)
print('query: ', query)
print('answer: ',answer.strip())
