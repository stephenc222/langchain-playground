#!/usr/bin/env python3

import pytesseract
import requests
import os
import json
import io
from PIL import Image

url = os.environ["BILL_IMAGE_URL"]
r = requests.get(url, stream=True)
image = Image.open(io.BytesIO(r.content))

# Extract text from Image using Tesseract
bill_text = pytesseract.image_to_string(image)

# Pass text to GPT-3 to get JSON response
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"""Bearer {os.environ["OPENAI_API_KEY"]}"""
}

# Set up GPT-3 request payload
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{ "role": "user", "content": f'''
    Turn this utility bill into valid JSON, easily dumping to JSON file with Python.
    Remove characters that would otherwise create invalid JSON.
    It has a total.
    Then simplify key names.
    No other output except only valid JSON:
    
    {bill_text}'''}],
    "max_tokens": 3024,
    "temperature": 0,
    "top_p": 1.0,
    "n": 1,
    "stop": "\n\n"
}

# Send request to GPT-3 API and get response
response = requests.post(url, headers=headers, json=payload).json()

json_dict = json.loads(response['choices'][0]['message']['content'])

# Write to json data file
with open('data.json', 'w') as f:
    json.dump(json_dict, f, indent=4)