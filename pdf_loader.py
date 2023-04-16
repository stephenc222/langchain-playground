#!/usr/bin/env python3

from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import OnlinePDFLoader
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

loader = OnlinePDFLoader("https://arxiv.org/pdf/2302.03803.pdf")
# data = loader.load()

index = VectorstoreIndexCreator().from_loaders([loader])


query = "what is the abstract of this research paper about?"

response = index.query(query)

print(query)
print(response)
