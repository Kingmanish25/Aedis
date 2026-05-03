class StateManager:
    def __init__(self):
        self.state = {}

    def get(self):
        return self.state

    def update(self, key, value):
        self.state[key] = value

    def reset(self):
        self.state = {}