class EventConsumer:
    def __init__(self, producer):
        self.producer = producer

    def stream(self):
        return self.producer.get_events()