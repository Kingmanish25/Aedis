class BobClient:
    def __init__(self):
        self.logs = []

    def log(self, step, msg):
        entry = f"[IBM BOB] {step}: {msg}"
        self.logs.append(entry)

    def get_logs(self):
        return self.logs