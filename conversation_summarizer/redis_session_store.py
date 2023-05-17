import json
from typing import Optional
from session import Session
from session_store import SessionStore


class RedisSessionStore(SessionStore):
    """
    A class for storing and loading chat sessions in a Redis store.

    Attributes:
        redis_client: A Redis client for storing and loading chat sessions.
    """

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def store_session(self, user_id: str, session_key: str, session: Session):
        """
        Stores a chat session in the Redis store.

        Args:
            user_id (str): The user ID associated with the session.
            session_key (str): The session key for storing the session.
            session (Session): The chat session to store.
        """
        session_data = session.to_dict()

        self.redis_client.hset(
            f"user_sessions:{user_id}", session_key, json.dumps(session_data)
        )

    def load_session(self, user_id: str, session_key: str) -> Optional[Session]:
        """
        Loads a chat session from the Redis store.

        Args:
            user_id (str): The user ID associated with the session.
            session_key (str): The session key for loading the session.

        Returns:
            Optional[Session]: The loaded chat session if found, otherwise None.
        """
        session_data = self.redis_client.hget(f"user_sessions:{user_id}", session_key)

        return Session(**json.loads(session_data)) if session_data else None
