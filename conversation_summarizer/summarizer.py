from typing import List, Tuple
from message import Message


class Summarizer:
    """
    A class representing a summarizer for chat messages.

    Attributes:
        model: The summary generation model.
        token_limit (int): Token limit for summarization.
        kwargs (dict): Additional keyword arguments for the model.
    """

    def __init__(self, model, token_limit: int = 3000, **kwargs):
        self.model = model
        self.token_limit = token_limit
        self.kwargs = kwargs

    def summarize(self, messages: List[Message]) -> Tuple[List[Message], List[Message]]:
        """
        Summarizes the provided messages using the model.

        Args:
            messages (List[Message]): List of messages to be summarized.

        Returns:
            Tuple[List[Message], List[Message]]: Summarized messages and remaining messages.
        """
        summaries = []
        remaining_messages = messages.copy()

        while remaining_messages:
            batch, remaining_messages = self._get_message_batch(remaining_messages)
            if not batch:
                break

            # Process messages into a suitable format for the model
            input_data = self._process_messages(batch)

            # Generate summary using the model
            summary = self.model.generate_summary(input_data, **self.kwargs)
            summaries.extend(summary)

        # Post-process the summary
        summary_messages = [Message.from_dict(msg) for msg in summaries]

        return summary_messages, remaining_messages

    def _get_message_batch(self, messages: List[Message]) -> Tuple[List[Message], List[Message]]:
        """
        Extracts a batch of messages within the token limit.

        Args:
            messages (List[Message]): List of messages to be batched.

        Returns:
            Tuple[List[Message], List[Message]]: Batch of messages and remaining messages.
        """
        token_count = 0
        batch = []
        index = 0

        for i, message in enumerate(messages):
            # Ensure we don't split user-assistant message pairs
            if message.role == "assistant" and index + 1 < len(messages):
                continue

            if token_count + message.token_count <= self.token_limit:
                batch.append(message)
                token_count += message.token_count
                index = i + 1
            else:
                break

        return batch, messages[index:]

    def _process_messages(self, messages: List[Message]) -> str:
        """
        Converts the list of messages into a string format suitable for the model.

        Args:
            messages (List[Message]): List of messages to be processed.

        Returns:
            str: Processed messages as a string.
        """
        conversation_str = "Please summarize this conversation between a user and an AI assistant. Make sure to include enough detail that the assistant doesn't lose context.\n\n"

        for message in messages:
            conversation_str += f"{message.role.upper()}: {message.content}\n"

        return conversation_str

    def _post_process_summary(self, summary: List[dict], messages: List[Message]) -> Tuple[
        List[Message], List[Message]]:
        """
        Post-processes the generated summary and converts it to a list of messages.

        Args:
            summary (List[dict]): List of summarized message dictionaries.
            messages (List[Message]): List of messages to be post-processed.

        Returns:
            Tuple[List[Message], List[Message]]: Post-processed summary messages and remaining messages.
        """
        new_summary = [Message.from_dict(msg) for msg in summary]
        remaining_messages = messages[-len(new_summary):]

        return new_summary, remaining_messages
