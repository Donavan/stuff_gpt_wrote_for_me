from message import Message


class Summarizer:
    def __init__(self, model, token_limit=3000, **kwargs):
        self.model = model
        self.token_limit = token_limit
        self.kwargs = kwargs

    def summarize(self, messages):
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

    def _get_message_batch(self, messages):
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

    def _process_messages(self, messages):
        # Create a string with the required structure
        conversation_str = "Please summarize this conversation between a user and an AI assistant. Make sure to include enough detail that the assistant doesn't lose context.\n\n"

        for message in messages:
            conversation_str += f"{message.role.upper()}: {message.content}\n"

        return conversation_str

    def _post_process_summary(self, summary, messages):
        # Perform any post-processing steps if needed
        new_summary = [Message.from_dict(msg) for msg in summary]
        remaining_messages = messages[-len(new_summary):]

        return new_summary, remaining_messages
