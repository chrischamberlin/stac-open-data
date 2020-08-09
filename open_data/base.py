from abc import ABC, abstractmethod


class StacCollectionProvider(ABC):

    @abstractmethod
    def collection(self):
        pass

    @abstractmethod
    def item(self, itemid):
        pass


