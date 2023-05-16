class Message:
    def __init__(self, role: str, content: str, timestamp: float):
        self.role = role
        self.content = content
        self.token_count = len(content)
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "token_count": self.token_count,
            "timestamp": self.timestamp,
        }
