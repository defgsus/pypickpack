from ..log import log
from .._2d import add_2d


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
        # log(f"{self}.on_picked({agent})")
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
        Called when another agent pushes this agent.
        The agent might not be in the world yet!
        :return: None
        """
        # log(f"{self}.on_pushed({agent})")
        pass

