import abc

class Exchange(metaclass=abc.ABCMeta):
    """Abstract exchange interface."""

    @abc.abstractmethod
    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        """Place an order and return execution details."""
        raise NotImplementedError

    @abc.abstractmethod
    def place_order_ioc(
        self, symbol: str, side: str, quantity: float, price: float | None = None
    ) -> dict:
        """Place an immediate-or-cancel order."""
        raise NotImplementedError
