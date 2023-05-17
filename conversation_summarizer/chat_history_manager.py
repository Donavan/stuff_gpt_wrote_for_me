import logging
from typing import Optional, Union
from session import Session


class ChatHistoryManager:
    """
    A class to manage chat sessions and their associated messages.

    Attributes:
        sessions (dict): A dictionary to store chat sessions.
        session_store: A storage service for storing and loading sessions.
    """

    def __init__(self, session_store):
        self.sessions = {}
        self.session_store = session_store

    def create_session(self, user_id: str, **kwargs) -> str:
        """
        Creates a new chat session.

        Args:
            user_id (str): The user ID associated with the session.
            **kwargs: Optional keyword arguments for creating a Session object.

        Returns:
            str: The session ID of the newly created session.
        """
        session = Session(user_id=user_id, **kwargs)
        self.sessions[session.session_id] = session
        self.session_store.store_session(user_id, session.session_id, session)

        logging.info(f"New session created: {session.session_id}")
        return session.session_id

    def get_session(self, user_id: str, session_id: str) -> Optional[Session]:
        """
        Retrieves a chat session.

        Args:
            user_id (str): The user ID associated with the session.
            session_id (str): The session ID to retrieve.

        Returns:
            Optional[Session]: The requested chat session if found, otherwise None.
        """
        if session_id not in self.sessions:
            session = self.session_store.load_session(user_id, session_id)

            if session:
                self.sessions[session_id] = session
            else:
                logging.error(f"Session not found: {session_id}")
                return None

        return self.sessions[session_id]

    def update_session(self, user_id: str, session: Session):
        """
        Updates a chat session by storing it in the session store.

        Args:
            user_id (str): The user ID associated with the session.
            session (Session): The chat session to update.
        """
        self.session_store.store_session(user_id, session.session_id, session)

    def get_messages(self, user_id: str, session_id: str, max_count: Optional[int] = None,
                     max_tokens: Optional[int] = None):
        """
        Retrieves messages from a chat session.

        Args:
            user_id (str): The user ID associated with the session.
            session_id (str): The session ID from which to retrieve messages.
            max_count (Optional[int], optional): Maximum number of messages to retrieve. Defaults to None.
            max_tokens (Optional[int], optional): Maximum number of tokens to retrieve. Defaults to None.

        Returns:
            Union[None, Any]: The retrieved messages if the session is found, otherwise None.
        """
        session = self.get_session(user_id, session_id)
        if session:
            return session.get_messages(max_count=max_count, max_tokens=max_tokens)
        else:
            return None
