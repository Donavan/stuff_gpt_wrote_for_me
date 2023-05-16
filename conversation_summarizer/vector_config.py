import json
from typing import Dict, Any


class VectorConfig:
    def __init__(self, index_name: str, k: int, min_relevance: float):
        self.index_name = index_name
        self.k = k
        self.min_relevance = min_relevance

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index_name': self.index_name,
            'k': self.k,
            'min_relevance': self.min_relevance
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            index_name=data['index_name'],
            k=data['k'],
            min_relevance=data['min_relevance']
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)
