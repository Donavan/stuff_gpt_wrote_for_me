from typing import Dict, Any

class Message:
    def __init__(self, content: str, role: str, created_at: str, token_count: int):
        self.content = content
        self.role = role
        self.created_at = created_at
        self.token_count = token_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            'content': self.content,
            'role': self.role,
            'created_at': self.created_at,
            'token_count': self.token_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            content=data['content'],
            role=data['role'],
            created_at=data['created_at'],
            token_count=data['token_count']
        )
