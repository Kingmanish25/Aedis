from collections import deque

class EventProducer:
    def __init__(self, max_events=1000):
        """
        Initialize event producer with a bounded queue.
        
        Args:
            max_events: Maximum number of events to keep in memory (default 1000)
        """
        self.events = deque(maxlen=max_events)
        self.consumers = []
        self.max_events = max_events

    def publish(self, event):
        """Publish an event to all registered consumers"""
        self.events.append(event)
        
        # Notify all consumers
        for consumer in self.consumers:
            try:
                consumer.handle_event(event)
            except Exception as e:
                print(f"Error in consumer {consumer}: {e}")

    def subscribe(self, consumer):
        """Register a consumer to receive events"""
        if consumer not in self.consumers:
            self.consumers.append(consumer)

    def unsubscribe(self, consumer):
        """Unregister a consumer"""
        if consumer in self.consumers:
            self.consumers.remove(consumer)

    def get_events(self, limit=None):
        """
        Get recent events.
        
        Args:
            limit: Maximum number of events to return (None for all)
        """
        if limit:
            return list(self.events)[-limit:]
        return list(self.events)
    
    def clear_events(self):
        """Clear all stored events"""
        self.events.clear()
    
    def get_events_by_source(self, source):
        """Get events from a specific source"""
        return [e for e in self.events if e.source == source]
    
    def get_events_by_type(self, event_type):
        """Get events of a specific type"""
        return [e for e in self.events if e.step == event_type]