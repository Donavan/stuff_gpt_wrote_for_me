import json
from typing import Dict, Any, List, Optional
from vector_config import VectorConfig


class ModelConfig:
    """
    A class representing a model configuration with model_name, tokens, vectors, and other_params.

    Attributes:
        model_name (str): The name of the model.
        tokens (int): The number of tokens in the model.
        vectors (List[VectorConfig]): A list of vector configurations.
        other_params (Dict[str, Any]): Other parameters related to the model configuration.
    """

    def __init__(self, model_name: str = "", tokens: int = 0, vectors: Optional[List[VectorConfig]] = None, **kwargs):
        self.model_name = model_name
        self.tokens = tokens
        self.vectors = vectors if vectors is not None else []
        self.other_params = kwargs

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the model configuration object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the model configuration.
        """
        data = self.other_params.copy()
        data.update({
            "model_name": self.model_name,
            "tokens": self.tokens,
            "vectors": [vector.to_dict() for vector in self.vectors],
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelConfig':
        """
        Creates a model configuration object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary representing a model configuration.

        Returns:
            ModelConfig: A model configuration object created from the dictionary.
        """
        model_name = data.pop("model_name", "")
        tokens = data.pop("tokens", 0)
        vectors_data = data.pop("vectors", [])
        vectors = [VectorConfig.from_dict(vector_data) for vector_data in vectors_data]
        return cls(model_name=model_name, tokens=tokens, vectors=vectors, **data)

    def to_json(self) -> str:
        """
        Converts the model configuration object to a JSON string.

        Returns:
            str: A JSON string representing the model configuration.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'ModelConfig':
        """
        Creates a model configuration object from a JSON string.

        Args:
            json_str (str): A JSON string representing a model configuration.

        Returns:
            ModelConfig: A model configuration object created from the JSON string.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)