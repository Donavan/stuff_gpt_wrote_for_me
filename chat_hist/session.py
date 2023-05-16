import time
import uuid
import logging
from message import Message
from model_config import ModelConfig


class Session:
    def __init__(self, user_id: str, **kwargs):
        self.user_id = user_id
        self.session_id = kwargs.get("session_id", str(uuid.uuid4()))
        self.name = kwargs.get("name", "New chat")
        self.model_config = kwargs.get("model_config", ModelConfig())
        self.created_at = time.time()
        self.last_updated = self.created_at
        self.messages = kwargs.get("messages", [])

    def add_message(self, message: Message):
        self.messages.append(message)
        self.last_updated = time.time()
        logging.info(f"Message added: {message.to_dict()}")

    def get_messages(self, max_count=None, max_tokens=None):
        messages = self.messages[::-1]

        if max_count is not None:
            messages = messages[:max_count]

        if max_tokens is not None:
            token_count = 0
            filtered_messages = []

            for message in messages:
                if token_count + message.token_count <= max_tokens:
                    token_count += message.token_count
                    filtered_messages.append(message)
                else:
                    break

            messages = filtered_messages

        return messages

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "name": self.name,
            "model_config": self.model_config.to_dict(),
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "messages": [message.to_dict() for message in self.messages]
        }
