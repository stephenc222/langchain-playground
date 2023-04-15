from tiktoken import get_encoding
from langchain.schema import ChatMessage

ENCODING = "cl100k_base"

class SlidingContextWindow:
    def __init__(self, max_tokens, model):
        self.max_tokens = max_tokens
        self.model = model
        self.encoding = get_encoding(ENCODING)
        self.messages = []
    def get_context_dict(self):
        """Get the current context for the model as a dictionary."""
        return {"messages": self.messages}

    def num_tokens_from_string(self, string: str) -> int:
        """Returns the number of tokens in a text string."""
        num_tokens = len(self.encoding.encode(string))
        return num_tokens

    def add_message(self, role, content):
        """Add a new message to the context."""
        message = {
            "role": role,
            "content": content
        }
        self.messages.append(message)
        self.truncate_messages()

    def truncate_messages(self):
        """Truncate messages to fit within the token limit."""
        total_tokens = 0
        truncated_messages = []
        for message in reversed(self.messages):
            message_tokens = self.num_tokens_from_string(message["content"])
            if total_tokens + message_tokens > self.max_tokens:
                break
            total_tokens += message_tokens
            truncated_messages.insert(0, message)
        self.messages = truncated_messages

    def get_context(self):
        """Get the current context for the model."""
        return self.messages
    def get_langchain_context(self):
        """Get the current context for the model."""
        # Convert messages to the expected format of ChatMessage
        chat_messages = [
            ChatMessage(role=msg['role'], content=msg['content'])
            for msg in self.messages
        ]
        return chat_messages


