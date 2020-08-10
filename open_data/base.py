from abc import ABC, abstractmethod

from typing import (
    Tuple,
    List,
    Dict,
    Optional)

class StacCollectionProvider(ABC):

    @abstractmethod
    def collection(self):
        pass

    @abstractmethod
    def item(self, itemid):
        pass

    @abstractmethod
    def item_list(self, page_token=None) -> Tuple[List[Dict], str]:
        pass
