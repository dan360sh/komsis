from abc import ABC, abstractmethod, abstractproperty


class AbstractDiscount(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractproperty
    def json_response(self):
        pass


class BaseDiscount(AbstractDiscount):
    def __init__(self, post_data, request, cart) -> None:
        self._data = post_data.copy()
        self._account = request.user.account
        self._cart = cart
        self._cart_count = 0
        self._has_errors = False
        self._json_response = dict()

    @property
    def json_response(self):
        return self._json_response
