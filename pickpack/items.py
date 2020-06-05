

from .agents import AgentBase


class ItemBase(AgentBase):

    _counter = dict()

    def __init__(self, id):
        super().__init__(id=f"{id}-{self.__class__._counter.get(id, 0)}")
        self.__class__._counter[id] = self.__class__._counter.get(id, 0) + 1

    def on_picked(self, world, agent):
        if agent.add_item(self):
            world.remove_agent(self)
            return True
        return False


class PickOrder(ItemBase):

    def __init__(self, item_lines):
        super().__init__("po")
        self.item_lines = item_lines


class Article(ItemBase):

    def __init__(self, asin):
        super().__init__(asin)
        self.asin = asin
