try:
    from lib.ai_client import OllamaChatClient
    from lib.brief_builder import HandoffBriefBuilder
except ImportError:
    from ai_client import OllamaChatClient
    from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        """Initialize the CLI application."""
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        """Print a welcome message and command guidance."""
        print("Shift Handoff Brief CLI")
        print("Create and revise AI-assisted shift handoff briefs.\n")
        print(self.command_help())

    def command_help(self):
        """Return command guidance as a string."""
        return (
            "Commands:\n"
            "  brief <shift notes>    Create a new handoff brief.\n"
            "  revise <feedback>     Revise the previous brief using feedback.\n"
            "  history               Show current conversation message count.\n"
            "  reset                 Clear conversation history.\n"
            "  help                  Show this command list.\n"
            "  exit or quit          Stop the program."
        )

    def handle_command(self, raw_input):
        """Route a user command."""
        if raw_input is None or not str(raw_input).strip():
            return "Input Error: Command cannot be empty."

        clean_input = str(raw_input).strip()
        parts = clean_input.split(maxsplit=1)
        command = parts[0].lower()
        payload = parts[1].strip() if len(parts) > 1 else ""

        try:
            if command == "brief":
                if not payload:
                    return "Input Error: Please provide shift notes (e.g., 'brief <shift notes>')."
                return self.brief_builder.create_brief(self.ai_client, payload)

            elif command == "revise":
                if not payload:
                    return "Input Error: Please provide revision feedback (e.g., 'revise <feedback>')."
                return self.brief_builder.revise_brief(self.ai_client, payload)

            elif command == "history":
                count = self.ai_client.message_count()
                return f"Conversation messages: {count}"

            elif command == "reset":
                self.ai_client.reset()
                return "Conversation history reset."

            elif command == "help":
                return self.command_help()

            elif command in ("exit", "quit"):
                self.running = False
                return "Goodbye!"

            else:
                return f"Input Error: Unknown command '{command}'. Type 'help' for available commands."

        except ValueError as ve:
            return f"Input Error: {ve}"
        except RuntimeError as re:
            return f"Service Error: {re}"

    def run(self):
        """Run the CLI input loop."""
        self.display_welcome()
        while self.running:
            try:
                user_input = input("\n> ")
                output = self.handle_command(user_input)
                if output:
                    print(output)
            except (EOFError, KeyboardInterrupt):
                self.running = False
                print("\nGoodbye!")


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()