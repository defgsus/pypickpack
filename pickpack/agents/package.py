from .base import AgentBase

from ..log import log
from .._2d import *


class Package(AgentBase):
    def __init__(self, id, max_items=5):
        super().__init__(id, max_items=max_items)

    def on_picked(self, world, agent):
        if not self.items:
            if agent.add_item(self):
                world.remove_agent(self)
                return True
            return False
        item = self.items.pop(-1)
        agent.add_item(item)
        return True

    def on_put(self, world, agent, item):
        if len(self.items) >= self.max_items:
            return False
        self.items.append(item)
        return True
