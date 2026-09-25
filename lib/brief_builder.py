class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def build_brief_prompt(self, notes):
        """Build a prompt for creating a new shift handoff brief."""
        if notes is None or not str(notes).strip():
            raise ValueError("Shift notes cannot be empty.")

        sections_str = "\n".join(self.REQUIRED_SECTIONS)
        return (
            f"You are a shift handoff assistant. Create a structured shift handoff brief using the following shift notes:\n\n"
            f"{str(notes).strip()}\n\n"
            f"Your response MUST include the following required section headings exactly as shown:\n"
            f"{sections_str}\n\n"
            f"Instructions:\n"
            f"- Do not invent unsupported details.\n"
            f"- Use 'Unknown' when details are not provided in the notes."
        )

    def build_revision_prompt(self, feedback):
        """Build a prompt for revising the previous handoff brief."""
        if feedback is None or not str(feedback).strip():
            raise ValueError("Revision feedback cannot be empty.")

        sections_str = "\n".join(self.REQUIRED_SECTIONS)
        return (
            f"Based on our previous conversation, please revise the shift handoff brief using this manager feedback:\n\n"
            f"{str(feedback).strip()}\n\n"
            f"Your revised response MUST include the following required section headings exactly as shown:\n"
            f"{sections_str}\n\n"
            f"Instructions:\n"
            f"- Do not invent unsupported details.\n"
            f"- Use 'Unknown' when details are missing."
        )

    def is_usable_brief(self, response_text):
        """Check whether the AI response includes the required handoff structure."""
        if response_text is None or not str(response_text).strip():
            return False

        text = str(response_text)
        return all(section in text for section in self.REQUIRED_SECTIONS)

    def format_brief(self, response_text):
        """Format a created handoff brief for display."""
        return f"\nShift Handoff Brief\n\n{response_text}"

    def format_revised_brief(self, response_text):
        """Format a revised handoff brief for display."""
        return f"\nRevised Shift Handoff Brief\n\n{response_text}"

    def create_brief(self, ai_client, notes):
        """Create a new handoff brief."""
        prompt = self.build_brief_prompt(notes)
        response = ai_client.send(prompt)
        if not self.is_usable_brief(response):
            raise RuntimeError("AI response did not include required sections.")
        return self.format_brief(response)

    def revise_brief(self, ai_client, feedback):
        """Revise the previous handoff brief."""
        prompt = self.build_revision_prompt(feedback)
        response = ai_client.send(prompt)
        if not self.is_usable_brief(response):
            raise RuntimeError("AI response did not include required sections.")
        return self.format_revised_brief(response)