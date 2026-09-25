import ollama


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        """Initialize the client with a model name and instance-specific message history."""
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        """Send a prompt to the AI service and return the assistant response text."""
        if prompt is None or not str(prompt).strip():
            raise ValueError("Prompt cannot be empty or whitespace only.")

        clean_prompt = str(prompt).strip()
        user_msg = {"role": "user", "content": clean_prompt}
        self.history.append(user_msg)

        try:
            response = ollama.chat(model=self.model_name, messages=self.history)

            # Support both object-style and dictionary-style responses
            if hasattr(response, "message"):
                msg = response.message
                content = msg.content if hasattr(msg, "content") else msg.get("content")
            elif isinstance(response, dict) and "message" in response:
                msg = response["message"]
                content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", None)
            else:
                content = None

            if content is None or not isinstance(content, str) or not content.strip():
                raise ValueError("AI service returned empty or invalid assistant content.")

            assistant_msg = {"role": "assistant", "content": content}
            self.history.append(assistant_msg)
            return content

        except Exception as e:
            # Rollback failed user message on failure
            if self.history and self.history[-1] == user_msg:
                self.history.pop()
            raise RuntimeError(f"AI service request failed: {e}") from e

    def reset(self):
        """Clear the conversation history."""
        self.history = []

    def message_count(self):
        """Return the number of messages currently stored in conversation history."""
        return len(self.history)

    def get_transcript(self):
        """Return a safe deep copy of the conversation history."""
        return [dict(msg) for msg in self.history]