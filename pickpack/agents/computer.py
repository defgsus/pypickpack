import random

from .base import AgentBase

from ..log import log
from .._2d import *


class Computer(AgentBase):
    def __init__(self, id):
        super().__init__(id, processing_fps=1)

    def on_picked(self, world, agent):
        pick_order = self.create_pick_order(world)
        agent.add_item(pick_order)
        return True

    def process(self, world, time_delta):
        if random.randrange(100) == 0:
            self.spit_pick_order(world)

    def create_pick_order(self, world):
        from .items import PickOrder

        shelves = world.agents.filter_by_class(Shelf)
        line_items = [
            random.choice(shelves).shelf_id
            for i in range(random.randint(1, 3))
        ]
        return PickOrder(line_items)

    def spit_pick_order(self, world):
        dir = (0, 1)
        pos = add_2d(self.position, dir)
        if not world.is_static_map_empty(pos):
            return
        agent = world.agent_map[pos[1]][pos[0]]
        if agent:
            if world.can_push_from_to(agent.position, add_2d(agent.position, dir)):
                world.agent_move(agent, dir, pushed_by=self)

        pick_order = self.create_pick_order(world)
        world.add_agent(pick_order, pos)

