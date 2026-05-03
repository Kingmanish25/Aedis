from app.config import Config

class Executor:
    def __init__(self):
        self.execution_count = 0
        
    def _validate_action(self, action):
        """
        Validate action against autonomous mode constraints.
        
        Returns: (is_valid, error_message)
        """
        if not action:
            return False, "Action is None or empty"
        
        action_type = action.get("type")
        if not action_type:
            return False, "Action type is missing"
        
        # Check if action type is allowed
        if action_type not in Config.ALLOWED_ACTIONS:
            return False, f"Action type '{action_type}' not in allowed actions: {Config.ALLOWED_ACTIONS}"
        
        # Check if we've exceeded max actions per run
        if self.execution_count >= Config.MAX_ACTIONS_PER_RUN:
            return False, f"Exceeded maximum actions per run ({Config.MAX_ACTIONS_PER_RUN})"
        
        return True, None
    
    def execute(self, action):
        """
        Execute an action with validation and constraint enforcement.
        
        Args:
            action: Dict containing action details (type, payload, etc.)
            
        Returns:
            Dict with execution result
        """
        # Validate action
        is_valid, error_msg = self._validate_action(action)
        if not is_valid:
            return {
                "status": "rejected",
                "reason": error_msg,
                "action": action
            }
        
        action_type = action.get("type")
        
        try:
            # Execute based on type
            if action_type == "notify":
                result = self._execute_notify(action)
            elif action_type == "report":
                result = self._execute_report(action)
            elif action_type == "simulate":
                result = self._execute_simulate(action)
            else:
                result = {
                    "status": "skipped",
                    "reason": f"Unsupported action type: {action_type}"
                }
            
            # Increment execution count on success
            if result.get("status") not in ["rejected", "skipped", "error"]:
                self.execution_count += 1
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "reason": f"Execution failed: {str(e)}",
                "action": action
            }
    
    def _execute_notify(self, action):
        """Simulate notification sending"""
        payload = action.get("payload", {})
        channel = payload.get("channel", "email")
        
        return {
            "status": "sent",
            "channel": channel,
            "payload": payload,
            "message": f"Notification sent via {channel}"
        }
    
    def _execute_report(self, action):
        """Simulate report generation"""
        payload = action.get("payload", {})
        report_type = payload.get("type", "summary")
        
        return {
            "status": "generated",
            "report_type": report_type,
            "payload": payload,
            "message": f"Report '{report_type}' generated successfully"
        }
    
    def _execute_simulate(self, action):
        """Simulate a scenario"""
        payload = action.get("payload", {})
        scenario = payload.get("scenario", "unknown")
        
        return {
            "status": "simulated",
            "scenario": scenario,
            "result": "Projected +12% recovery",
            "message": f"Simulation for '{scenario}' completed"
        }
    
    def reset(self):
        """Reset execution counter"""
        self.execution_count = 0
    
    def get_execution_count(self):
        """Get current execution count"""
        return self.execution_count