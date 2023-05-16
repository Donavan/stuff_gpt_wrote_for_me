import json


class ModelConfig:
    def __init__(self, **kwargs):
        self.model_name = kwargs.get("model_name", "gpt-3.5-turbo")
        self.temperature = kwargs.get("temperature", 1.0)
        self.frequency_penalty = kwargs.get("frequency_penalty", 0.0)
        self.presence_penalty = kwargs.get("presence_penalty", 0.0)
        self.ai_custom_name = kwargs.get("ai_custom_name", "")
        self.prompt_prefix = kwargs.get("prompt_prefix", "")

    def to_dict(self):
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "ai_custom_name": self.ai_custom_name,
            "prompt_prefix": self.prompt_prefix,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_data):
        return cls(**json.loads(json_data))