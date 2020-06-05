import random

from .log import log


class AgentBase:

    def __init__(
            self,
            id,
            pushable=True,
            processing_fps=0,
            max_items=9,
    ):
        """
        Creates a new agent at position (0, 0)
        :param id: str, should be unique in the world (although it's not used yet)
        :param pushable: bool, can be pushed around
        :param processing_fps: int, number of calls to process() functions per second
        :param max_items: int, maximum number of items in inventory
        """
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
        self.max_items = max_items

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
        """
        Override to perform actions.

        The world contains the complete current state and all other agents.

        You can move the agent via world.agent_move(), pick with world.agent_pick() a.s.o.
        Please only move once per process call to make it fair.

        :param world: World instance
        :param time_delta: float, time since last call
        :return: None
        """
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
            If True, than the agent will loose the item
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


class Computer(AgentBase):
    def __init__(self, id):
        super().__init__(id)

    def on_picked(self, world, agent):
        from .items import PickOrder

        shelves = world.agents.filter_by_class(Shelf)
        line_items = [
            random.choice(shelves).shelf_id
            for i in range(random.randint(1, 3))
        ]
        pick_order = PickOrder(line_items)

        agent.add_item(pick_order)
        return True


class Shelf(AgentBase):
    def __init__(self, shelf_id, max_items=20):
        from .items import Article
        super().__init__(f"shelf-{shelf_id}", pushable=False, max_items=max_items)
        self.shelf_id = shelf_id
        self.items = [
            Article(f"B0{self.shelf_id}")
            for i in range(10)
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


class Agents:

    def __init__(self, world):
        self.world = world
        self.agents = []

    def __iter__(self):
        return iter(self.agents)

    def __len__(self):
        return len(self.agents)

    def __getitem__(self, i):
        return self.agents[i]

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

    def filter_by_class(self, *classes):
        ret = Agents(self.world)
        ret.agents = list(filter(
            lambda a: isinstance(a, classes),
            self.agents
        ))
        return ret

