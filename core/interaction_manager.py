# core/interaction_manager.py

from core.dispatcher import dispatch
from commands import timer_manager

class InteractionManager:
    def __init__(self):
        # Stores context for follow-up interactions (like "How long?" after "Set timer")
        self.pending_confirmation = None

    def process(self, user_input: str) -> str:
        """
        Handles user input and delegates to dispatcher or manages follow-up interactions.
        """

        # Example: handle follow-up prompts
        if self.pending_confirmation:
            action = self.pending_confirmation.get("action")

            # Timer Follow-up (you can add more actions here)
            if action == "set_timer":
                duration = user_input.strip()
                self.pending_confirmation = None
                                
                return timer_manager.set_timer(duration)

        # General command processing
        result = dispatch(user_input)

        # Optional: detect actions that need follow-up
        if "timer" in user_input.lower() and "how long" in result.lower():
            self.pending_confirmation = {"action": "set_timer"}

        return result or "🤖 Sorry, I couldn't understand your command."
