# Conversational Summarizer

A Python library to summarize conversations between a user and an AI assistant.

NOTE FROM THE HUMAN: This is a WIP and not at all tested.  Aside from this blurb, GPT-4 has written everything else you see in this tree. The file CHAT_LOG.md contains a running log of this process.


## Classes

- `Message`: Class representing a single conversation message.
- `ModelConfig`: Class representing the model configuration.
- `VectorConfig`: Class representing vector indexing configuration (optional).
- `Summarizer`: Class responsible for summarizing input conversations using the provided model.

## Usage

### Message

Create a new `Message` object:

```python
from message import Message

content = "Hello, I need help with my order."
role = "user"
created_at = "2022-06-24T10:30:00Z"
token_count = 12

message = Message(content=content, role=role, created_at=created_at, token_count=token_count)
```

Convert a `Message` object to a dictionary:

```python
message_dict = message.to_dict()
```

Create a `Message` object from a dictionary:

```python
message_obj = Message.from_dict(message_dict)
```

### ModelConfig

Create a new `ModelConfig` object:

```python
from model_config import ModelConfig
from vector_config import VectorConfig

model_name = "model_name"
tokens = 100

vector_id = VectorConfig(index_name="index_name", k=5, min_relevance=0.8)

model_config = ModelConfig(model_name=model_name, tokens=tokens, vectors=[vector_id])
```

Convert a `ModelConfig` object to a dictionary:

```python
model_config_dict = model_config.to_dict()
```

Create a `ModelConfig` object from a dictionary:

```python
model_config_obj = ModelConfig.from_dict(model_config_dict)
```

### Summarizer

Create a new `Summarizer` object with a model and a token limit:

```python
from summarizer import Summarizer

model = SomeModel()
token_limit = 3000

summarizer = Summarizer(model, token_limit)
```

Summarize a list of `Message` objects:

```python
messages = [message1, message2, message3]

summary_result, remaining_messages = summarizer.summarize(messages)
```

### VectorConfig (Optional)

Create a new `VectorConfig` object:

```python
from vector_config import VectorConfig

index_name = "index_name"
k = 5
min_relevance = 0.8

vector_config = VectorConfig(index_name=index_name, k=k, min_relevance=min_relevance)
```

Convert a `VectorConfig` object to a dictionary:

```python
vector_config_dict = vector_config.to_dict()
```

Create a `VectorConfig` object from a dictionary:

```python
vector_config_obj = VectorConfig.from_dict(vector_config_dict)
```

## Installation

To install the Conversational Summarizer library, follow these steps:

1. Clone the repository.

    ```
    git clone https://github.com/your-username/conversational_summarizer.git
    ```

2. Change the directory to the cloned repository.

    ```
    cd conversational_summarizer
    ```

3. Install the required dependencies.

    ```
    pip install -r requirements.txt
    ```

## Example

A simple example on how to use the Conversational Summarizer:

```python
from message import Message
from model_config import ModelConfig
from vector_config import VectorConfig
from summarizer import Summarizer

# Initialize the input messages.
messages = [
    Message(content="Hello, I need help with my order.", role="user", created_at="2022-06-24T10:30:00Z", token_count=12),
    Message(content="Sure, how may I help you?", role="assistant", created_at="2022-06-24T10:30:10Z", token_count=7),
    Message(content="Can you tell me when my order will arrive?", role="user", created_at="2022-06-24T10:30:30Z", token_count=12)
    ]

# Initialize the model configuration.
model_name = "model_name"
tokens = 100
vector_config = VectorConfig(index_name="index_name", k=5, min_relevance=0.8)
model_config = ModelConfig(model_name=model_name, tokens=tokens, vectors=[vector_config])

# ... load or create the model (e.g., OpenAI API, Hugging Face, or custom model)
model = load_or_create_model(model_config)

# Initialize the summarizer with the model and a token limit.
token_limit = 3000
summarizer = Summarizer(model=model, token_limit=token_limit)

# Summarize the input conversation.
summary_result, remaining_messages = summarizer.summarize(messages)

# Display the summary result.
print(f"Summary result: {summary_result}")

# Display any remaining messages.
print(f"Remaining messages: {[msg.content for msg in remaining_messages]}")
```

Replace `load_or_create_model` with the appropriate function or method to load or create your model instance.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contributing

Contributions are welcome! Please open an issue or create a pull request with your proposed changes. Make sure to follow the coding style and update the README if necessary.

## Support

If you have any questions or issues, feel free to open an issue on GitHub or reach out to the author via email or other relevant channels.


