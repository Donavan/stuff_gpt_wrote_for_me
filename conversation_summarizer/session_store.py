import abc
from typing import Optional
from session import Session


class SessionStore(abc.ABC):
    @abc.abstractmethod
    def store_session(self, user_id: str, session_key: str, session: Session) -> None:
        """
        Store the session object associated with a user_id and session_key.

        Args:
            user_id (str): User identifier.
            session_key (str): Session identifier.
            session (Session): Session object.
        """
        pass

    @abc.abstractmethod
    def load_session(self, user_id: str, session_key: str) -> Optional[Session]:
        """
        Load the session object associated with a user_id and session_key.

        Args:
            user_id (str): User identifier.
            session_key (str): Session identifier.

        Returns:
            Optional[Session]: Session object if found, None otherwise.
        """
        pass
