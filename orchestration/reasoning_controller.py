from app.config import Config

class ReasoningController:
    def __init__(self):
        self.loops = 0

    def should_continue(self, state):
        self.loops += 1

        if state.get("confidence", 0) >= Config.CONFIDENCE_THRESHOLD:
            return False

        if state.get("iteration", 0) >= Config.MAX_LOOPS:
            return False

        if state.get("error"):
            return True

        return False