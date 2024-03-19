from typing import Any, List

class Observable:
    """
    Represents an observable object that can be subscribed to by observers.
    """

    def __init__(self) -> None:
        """
        Initializes the Observable object.
        """
        self._observers: List[Observer] = []

    def subscribe(self, observer: 'Observer') -> None:
        """
        Subscribes an observer to this Observable object.

        Arguments:
            observer (Observer): The observer to subscribe.
        """
        self._observers.append(observer)

    def notify_observers(self, message, *args: Any, **kwargs: Any) -> None:
        """
        Notifies all subscribed observers with given arguments.

        Arguments:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        for observer in self._observers:
            observer.notify(message, self, *args, **kwargs)

    def unsubscribe(self, observer: 'Observer') -> None:
        """
        Unsubscribes an observer from this Observable object.

        Arguments:
            observer (Observer): The observer to unsubscribe.
        """
        self._observers.remove(observer)

class Observer:
    """
    Represents an observer that can be notified by observables.
    """

    def __init__(self, observable: Observable) -> None:
        """
        Initializes the Observer object and subscribes it to the given Observable.

        Arguments:
            observable (Observable): The observable to subscribe to.
        """
        observable.subscribe(self)

    def notify(self, message: str, observable: Observable, *args: Any, **kwargs: Any) -> None:
        """
        Notifies the observer with given arguments.

        Arguments:
            observable (Observable): The observable notifying the observer.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        print(f'{message}', args, kwargs, 'received by: ', observable.__class__.__name__)
