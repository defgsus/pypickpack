from .base import AgentBase

from ..log import log
from .._2d import *


class Player(AgentBase):
    def __init__(self, id):
        super().__init__(id)
        self.selected_item_index = 0

    def copy(self):
        c = super().copy()
        c.selected_item_index = self.selected_item_index
        return c

    def selected_item(self):
        if self.selected_item_index < len(self.items):
            return self.items[self.selected_item_index]
        return None

    def remove_item(self, item):
        super().remove_item(item)
        self.selected_item_index = max(0, min(self.selected_item_index, len(self.items) - 1))
