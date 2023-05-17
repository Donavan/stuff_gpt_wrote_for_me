from typing import Dict, Any


class Message:
    """
    A class representing a message with content, role, creation time, and token count.

    Attributes:
        content (str): The content of the message.
        role (str): The role of the sender.
        created_at (str): The creation time of the message.
        token_count (int): The token count of the message.
    """

    def __init__(self, content: str, role: str, created_at: str, token_count: int):
        self.content = content
        self.role = role
        self.created_at = created_at
        self.token_count = token_count

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the message object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the message object.
        """
        return {
            'content': self.content,
            'role': self.role,
            'created_at': self.created_at,
            'token_count': self.token_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """
        Creates a message object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary representing a message object.

        Returns:
            Message: A message object created from the dictionary.
        """
        return cls(
            content=data['content'],
            role=data['role'],
            created_at=data['created_at'],
            token_count=data['token_count']
        )
