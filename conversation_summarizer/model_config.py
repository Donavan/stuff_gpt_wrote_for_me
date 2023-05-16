import json
from typing import Dict, Any, List, Optional
from vector_config import VectorConfig

class ModelConfig:
    def __init__(self, model_name: str = "", tokens: int = 0, vectors: Optional[List[VectorConfig]] = None, **kwargs):
        self.model_name = model_name
        self.tokens = tokens
        self.vectors = vectors if vectors is not None else []
        self.other_params = kwargs

    def to_dict(self) -> Dict[str, Any]:
        data = self.other_params.copy()
        data.update({
            "model_name": self.model_name,
            "tokens": self.tokens,
            "vectors": [vector.to_dict() for vector in self.vectors],
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        model_name = data.pop("model_name", "")
        tokens = data.pop("tokens", 0)
        vectors_data = data.pop("vectors", [])
        vectors = [VectorConfig.from_dict(vector_data) for vector_data in vectors_data]
        return cls(model_name=model_name, tokens=tokens, vectors=vectors, **data)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)
