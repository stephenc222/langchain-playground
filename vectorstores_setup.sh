#!/usr/bin/env bash

# Install other dependencies
# https://github.com/Unstructured-IO/unstructured/blob/main/docs/source/installing.rst
brew install libmagic && \
brew install poppler && \
brew install tesseract && \
# If parsing xml / html documents:
brew install libxml2 && \
brew install libxslt 
