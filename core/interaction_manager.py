# core/interaction_manager.py

from core.dispatcher import dispatch
from commands import timer_manager

class InteractionManager:
    def __init__(self):
        self.pending_confirmation = None

    def process(self, user_input: str) -> str:
        if self.pending_confirmation:
            action = self.pending_confirmation.get("action")
            if action == "set_timer":
                duration = user_input.strip()
                self.pending_confirmation = None
                return timer_manager.set_timer(duration)

        result = dispatch(user_input)

        if "timer" in user_input.lower() and "how long" in str(result).lower():
            self.pending_confirmation = {"action": "set_timer"}

        return result or ""

# ✅ Global shared instance
interaction_manager_instance = InteractionManager()
