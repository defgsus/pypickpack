from .base import AgentBase

from ..log import log
from .._2d import *


class Shelf(AgentBase):
    def __init__(self, shelf_id, max_items=20, num_items=10):
        super().__init__(f"shelf-{shelf_id}", pushable=False, max_items=max_items)
        from ..items import Article
        self.shelf_id = shelf_id
        self.items = [
            Article(f"B0{self.shelf_id}")
            for i in range(num_items)
        ]

    def on_picked(self, world, agent):
        if not self.items:
            return False
        item = self.items.pop(-1)
        agent.add_item(item)
        return True

    def on_put(self, world, agent, item):
        if len(self.items) >= self.max_items:
            return False
        self.items.append(item)
        return True

