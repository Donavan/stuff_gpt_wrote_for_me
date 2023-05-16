import time
import uuid
import logging
from message import Message
from model_config import ModelConfig


class Session:
    def __init__(self, user_id: str, **kwargs):
        self.user_id = user_id
        self.session_id = kwargs.get("session_id", str(uuid.uuid4()))
        self.name = kwargs.get("name", f"Session {self.session_id[:8]}")
        self.model_config = kwargs.get("model_config", ModelConfig())
        self.created_at = kwargs.get("created_at", time.time())
        self.last_updated = kwargs.get("last_updated", self.created_at)
        self.messages = kwargs.get("messages", [])
        self.full_message_history = kwargs.get("full_message_history", self.messages.copy())
        self.summarizer = kwargs.get("summarizer", None)
        self.summary = kwargs.get("summary", [])
        self.max_tokens = kwargs.get("max_tokens", None)
        self.last_summary_index = kwargs.get("last_summary_index", 0)

    def add_message(self, message: Message):
        self.messages.append(message)
        self.full_message_history.append(message)
        self.last_updated = time.time()
        logging.info(f"Message added: {message.to_dict()}")

        total_tokens = sum(msg.token_count for msg in self.messages[self.last_summary_index:])
        if self.max_tokens is not None and total_tokens > self.max_tokens:
            self.summarize()

    def get_messages(self, max_count=None, max_tokens=None, use_summary=True):
        messages = self.messages[::-1]

        if use_summary:
            messages_with_summary = self.summary + messages
            messages = messages_with_summary

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

    def summarize(self):
        new_summary, remaining_messages = self.summarizer(self.full_message_history, max_tokens=self.max_tokens)
        self.summary += new_summary
        self.messages = self.full_message_history[-len(remaining_messages):]
        self.last_summary_index = len(self.full_message_history) - len(remaining_messages)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "name": self.name,
            "model_config": self.model_config.to_dict(),
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "messages": [message.to_dict() for message in self.messages],
            "summary": self.summary
        }
