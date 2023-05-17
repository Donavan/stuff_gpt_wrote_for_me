import time
import uuid
import logging
from typing import List, Optional
from message import Message
from model_config import ModelConfig


class Session:
    """
    A class representing a chat session with messages, user ID and model configuration.

    Attributes:
        user_id (str): The user ID associated with the session.
        session_id (str): The unique identifier for the chat session.
        name (str): The name of the chat session.
        model_config (ModelConfig): The configuration of the model used in the chat.
        created_at (float): Timestamp when the chat session was created.
        last_updated (float): Timestamp when the chat session was last updated.
        messages (List[Message]): A list of messages in the chat session.
        full_message_history (List[Message]): A list of all messages including summaries.
        summarizer: A function for summarizing the chat session.
        summary (List[str]): A list of summary messages.
        max_tokens (Optional[int]): Maximum number of tokens allowed in a chat session.
        last_summary_index (int): Index of the last summary in the full message history.
    """

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
        """
        Adds a message to the chat session and updates the last_updated timestamp.

        Args:
            message (Message): The message to add to the chat session.
        """
        self.messages.append(message)
        self.full_message_history.append(message)
        self.last_updated = time.time()
        logging.info(f"Message added: {message.to_dict()}")

        total_tokens = sum(msg.token_count for msg in self.messages[self.last_summary_index:])
        if self.max_tokens is not None and total_tokens > self.max_tokens:
            self.summarize()

    def get_messages(self, max_count: Optional[int] = None, max_tokens: Optional[int] = None, use_summary: bool = True) -> List[Message]:
        """
        Retrieves messages from the chat session, optionally using summary and limiting by count or tokens.

        Args:
            max_count (Optional[int], optional): Maximum number of messages to retrieve. Defaults to None.
            max_tokens (Optional[int], optional): Maximum number of tokens to retrieve. Defaults to None.
            use_summary (bool, optional): Whether to use the summary in the retrieved messages. Defaults to True.

        Returns:
            List[Message]: A list of messages that meet the given requirements.
        """
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
        """
        Summarizes the chat session and updates message lists and last_summary_index.
        """
        new_summary, remaining_messages = self.summarizer(self.full_message_history, max_tokens=self.max_tokens)
        self.summary += new_summary
        self.messages = self.full_message_history[-len(remaining_messages):]
        self.last_summary_index = len(self.full_message_history) - len(remaining_messages)

    def to_dict(self) -> dict:
        """
        Converts the chat session object to a dictionary.

        Returns:
            dict: A dictionary representing the chat session.
        """
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