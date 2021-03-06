from .base import ItemBase


class PickOrder(ItemBase):

    def __init__(self, item_lines):
        super().__init__("po")
        self.item_lines = item_lines

    def __str__(self):
        return f"{self.__class__.__name__}({self.item_lines})"

    def _copy_construct(self):
        return self.__class__(item_lines=self.item_lines)
