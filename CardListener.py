from abc import abstractmethod, ABC


class CardListener(ABC):
    @abstractmethod
    def card_is_presented(self, uid: str):
        pass