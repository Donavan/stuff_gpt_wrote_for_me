import logging
from session import Session


class ChatHistoryManager:
    def __init__(self, session_store):
        self.sessions = {}
        self.session_store = session_store

    def create_session(self, user_id: str, **kwargs) -> str:
        session = Session(user_id=user_id, **kwargs)
        self.sessions[session.session_id] = session
        self.session_store.store_session(user_id, session.session_id, session)

        logging.info(f"New session created: {session.session_id}")
        return session.session_id

    def get_session(self, user_id: str, session_id: str) -> Session | None:
        if session_id not in self.sessions:
            session = self.session_store.load_session(user_id, session_id)

            if session:
                self.sessions[session_id] = session
            else:
                logging.error(f"Session not found: {session_id}")
                return None

        return self.sessions[session_id]

    def update_session(self, user_id: str, session: Session):
        self.session_store.store_session(user_id, session.session_id, session)

    def get_messages(self, user_id: str, session_id: str, max_count=None, max_tokens=None):
        session = self.get_session(user_id, session_id)
        return session.get_messages(max_count=max_count, max_tokens=max_tokens)
