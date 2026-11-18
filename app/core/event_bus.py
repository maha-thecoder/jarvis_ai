from collections import defaultdict
from typing import Callable, Type


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type: Type, handler: Callable):
        self._subscribers[event_type].append(handler)

    def publish(self, event):
        handlers = self._subscribers.get(type(event), [])

        for handler in handlers:
            handler(event)