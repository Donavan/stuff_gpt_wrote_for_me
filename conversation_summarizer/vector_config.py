import json
from typing import Dict, Any


class VectorConfig:
    """
    A class representing the vector configuration for a search index.

    Attributes:
        index_name (str): The name of the search index.
        k (int): The number of results to return.
        min_relevance (float): The minimum relevance score to consider a result relevant.
    """

    def __init__(self, index_name: str, k: int, min_relevance: float) -> None:
        self.index_name = index_name
        self.k = k
        self.min_relevance = min_relevance

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the vector configuration to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the vector configuration.
        """
        return {
            'index_name': self.index_name,
            'k': self.k,
            'min_relevance': self.min_relevance
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorConfig':
        """
        Creates a VectorConfig object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing the vector configuration data.

        Returns:
            VectorConfig: A VectorConfig object.
        """
        return cls(
            index_name=data['index_name'],
            k=data['k'],
            min_relevance=data['min_relevance']
        )

    def to_json(self) -> str:
        """
        Converts the vector configuration to a JSON string.

        Returns:
            str: A JSON string representing the vector configuration.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'VectorConfig':
        """
        Creates a VectorConfig object from a JSON string.

        Args:
            json_str (str): A JSON string containing the vector configuration data.

        Returns:
            VectorConfig: A VectorConfig object.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
