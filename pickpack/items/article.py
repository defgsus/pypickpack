from .base import ItemBase


class Article(ItemBase):

    def __init__(self, asin):
        super().__init__(asin)
        self.asin = asin

    def _copy_construct(self):
        return self.__class__(asin=self.asin)
