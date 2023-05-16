import json
from session import Session
from session_store import SessionStore


class RedisSessionStore(SessionStore):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def store_session(self, user_id: str, session_key: str, session: Session):
        session_data = session.to_dict()

        self.redis_client.hset(
            f"user_sessions:{user_id}", session_key, json.dumps(session_data)
        )

    def load_session(self, user_id: str, session_key: str) -> Session:
        session_data = self.redis_client.hget(f"user_sessions:{user_id}", session_key)

        return Session(**json.loads(session_data)) if session_data else None
