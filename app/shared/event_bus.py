from collections import defaultdict
from typing import Callable, Type, Any


class Event:
    """Base class for all events."""
    pass


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[Type[Event], list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], handler: Callable[[Event], None]) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        for handler in self._subscribers[type(event)]:
            handler(event)


event_bus = EventBus()