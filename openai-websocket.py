import asyncio
import websockets
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
HOST = 'localhost'
PORT = 8765

# NOTE: would put this in a Redis cache instead, but in-memory local cache here for testing out OpenAI
# and mostly written by GPT-3!
user_message_cache = {}

chat_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


async def chat(websocket):
    try:
        connection_id = id(websocket)
        if not connection_id in user_message_cache:
            user_message_cache[connection_id] = chat_messages.copy()

        async for message in websocket:
            response = await generate_response(connection_id, message)
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
        del user_message_cache[connection_id]
    except Exception as e:
        print(f"Error: {e}")



async def generate_response(connection_id, message):
    try:
        print('USER:', message)
        user_message = { "role": "user", "content": str(message) }
        user_message_cache[connection_id].append(user_message)
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=user_message_cache[connection_id],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        message = completions.choices[0].message
        user_message_cache[connection_id].append(message)
        message_text = completions.choices[0].message.content.strip()
        print('AI:', message_text)
        return message_text
    except Exception as e:
        print(f"Error generating response: {e}")

start_server = websockets.serve(chat, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
