import abc
from session import Session


class SessionStore(abc.ABC):
    @abc.abstractmethod
    def store_session(self, user_id: str, session_key: str, session: Session):
        """
        Store the session object associated with a user_id and session_key.
        :param user_id: User identifier.
        :param session_key: Session identifier.
        :param session: Session object.
        """
        pass

    @abc.abstractmethod
    def load_session(self, user_id: str, session_key: str) -> Session:
        """
        Load the session object associated with a user_id and session_key.
        :param user_id: User identifier.
        :param session_key: Session identifier.
        :return: Session object.
        """
        pass
