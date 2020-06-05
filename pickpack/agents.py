
from .log import log


class AgentBase:

    def __init__(
            self,
            id,
            pushable=True,
            processing_fps=0,
    ):
        self.id = id
        self.x = 0
        self.y = 0
        self.dir_x = 0
        self.dir_y = -1
        self.agents = None
        self.pushable = pushable
        self.processing_fps = processing_fps
        self._last_processing_time = -processing_fps
        self.items = []
        self.max_items = 10
    def __str__(self):
        return f"{self.__class__.__name__}({repr(self.id)})"

    @property
    def position(self):
        return self.x, self.y

    @property
    def direction(self):
        return self.dir_x, self.dir_y

    def stats_str(self):
        return f"{self.id}: {self.position} -> {self.direction}"

    def add_item(self, item):
        """
        Add an item to the inventory of the agent
        :param item: ItemBase instance
        :return: bool, False if no space left
        """
        if len(self.items) < self.max_items:
            self.items.insert(0, item)
            return True
        return False

    def remove_item(self, item):
        """
        Removes an item from inventory
        :param item: ItemBase instance
        :return: bool
        """
        idx = self.items.index(item)
        if idx >= 0:
            self.items.pop(idx)
            return True
        return False

    def is_inventory_full(self):
        return len(self.items) >= self.max_items

    def process(self, world, time_delta):
        pass

    def on_picked(self, world, agent):
        """
        Called when another agent picks this agent.
        The agent will/must have available space in inventory.
        :return: bool, True if something happened
        """
        # log(f"{self}.on_pick({agent})")
        return False

    def on_put(self, world, agent, item):
        """
        Called when another agent puts an item into this agent.
        The item will/must be in the agent's inventory.
        :return: bool, True if something happened
        """
        # log(f"{self}.on_put({agent})")
        return False

    def on_pushed(self, world, agent):
        """
        Called when another agent pushes this agent
        :return: bool
        """
        # log(f"{self}.on_pushed({agent})")
        pass


class Player(AgentBase):
    def __init__(self, id):
        super().__init__(id)
        self.selected_item_index = 0

    def selected_item(self):
        if self.selected_item_index < len(self.items):
            return self.items[self.selected_item_index]
        return None

    def remove_item(self, item):
        super().remove_item(item)
        self.selected_item_index = max(0, min(self.selected_item_index, len(self.items) - 1))


class Package(AgentBase):
    def __init__(self, id):
        super().__init__(id)


class Computer(AgentBase):
    def __init__(self, id):
        super().__init__(id)

    def on_picked(self, world, agent):
        from .items import PickOrder
        pick_order = PickOrder(
            ["TODO"]
        )
        agent.add_item(pick_order)
        return True


class Shelf(AgentBase):
    def __init__(self, shelf_id):
        from .items import Article
        super().__init__(f"shelf{shelf_id}", pushable=False)
        self.shelf_id = shelf_id
        self.content = [
            Article(f"B0{self.shelf_id}")
            for i in range(10)
        ]
        self.max_content = 20

    def on_picked(self, world, agent):
        if not self.content:
            return False
        item = self.content.pop(-1)
        agent.add_item(item)
        return True

    def on_put(self, world, agent, item):
        if len(self.content) >= self.max_content:
            return False
        agent.remove_item(item)
        self.content.append(item)


class Agents:

    def __init__(self, world):
        self.world = world
        self.agents = []

    def __iter__(self):
        return iter(self.agents)

    def __len__(self):
        return len(self.agents)

    def add_agent(self, agent):
        agent.agents = self
        self.agents.append(agent)

    def remove_agent(self, agent):
        i = self.agents.index(agent)
        if i >= 0:
            self.agents.pop(i)
        else:
            raise ValueError(f"Can not remove non-existent {agent}")

    def get_agent_at(self, x, y):
        for a in self.agents:
            if a.x == x and a.y == y:
                return a
        return None

