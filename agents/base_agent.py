class BaseAgent:
    def __init__(self, name, llm, bob, event_bus=None):
        self.name = name
        self.llm = llm
        self.bob = bob
        self.event_bus = event_bus

    def emit(self, step, message, data=None):
        if self.event_bus:
            from event_bus.schemas import Event
            self.event_bus.publish(Event(self.name, step, message, data))

    def run(self, state):
        raise NotImplementedError