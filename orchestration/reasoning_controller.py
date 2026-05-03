from app.config import Config

class ReasoningController:
    def __init__(self):
        self.loops = 0

    def should_continue(self, state):
        """
        Determine if the reasoning loop should continue.
        
        Returns True if:
        - There's an error that needs fixing
        - Confidence is below threshold AND we haven't exceeded max loops
        
        Returns False if:
        - Confidence threshold is met
        - Max loops exceeded
        - No error and confidence is acceptable
        """
        self.loops += 1
        
        current_iteration = state.get("iteration", 0)
        confidence = state.get("confidence", 0)
        has_error = state.get("error") is not None

        # Stop if we've reached high confidence
        if confidence >= Config.CONFIDENCE_THRESHOLD:
            return False

        # Stop if we've exceeded max loops
        if current_iteration >= Config.MAX_LOOPS:
            return False

        # Continue if there's an error to fix
        if has_error:
            return True

        # Continue if confidence is low and we have iterations left
        if confidence < Config.CONFIDENCE_THRESHOLD and current_iteration < Config.MAX_LOOPS:
            return True

        # Default: stop
        return False
    
    def reset(self):
        """Reset the loop counter"""
        self.loops = 0