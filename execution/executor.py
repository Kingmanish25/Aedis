class Executor:
    def execute(self, action):
        t = action.get("type")

        if t == "notify":
            # simulate notification
            return {"status": "sent", "channel": "email/slack", "payload": action.get("payload")}

        if t == "report":
            # simulate report generation
            return {"status": "generated", "report": action.get("payload")}

        if t == "simulate":
            # simulate a scenario
            return {"status": "simulated", "result": "Projected +12% recovery"}

        return {"status": "skipped", "reason": "unsupported action"}