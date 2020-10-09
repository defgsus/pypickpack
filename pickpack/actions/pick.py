from .base import ActionBase
from .._2d import distance, manhatten_distance, direction_int
from ..astar import astar_search


class PickDirection(ActionBase):

    def __init__(self, direction):
        super().__init__(direction=direction)
        self.has_picked = False

    def get_estimated_cost(self, world, agent):
        return 1

    def is_finished(self, world, agent):
        return self.has_picked

    def execute(self, world, agent):
        self.has_picked = world.agent_pick(agent, self.parameters["direction"])
        return self.has_picked


class PutDirection(ActionBase):

    def __init__(self, direction, item_id):
        super().__init__(direction=direction, item_id=item_id)
        self.has_put = False

    def get_estimated_cost(self, world, agent):
        return 1

    def is_finished(self, world, agent):
        return self.has_put

    def execute(self, world, agent):
        item = agent.item_by_id(self.parameters["item_id"])
        if not item:
            return False
        self.has_put = world.agent_put(agent, self.parameters["direction"], item)
        return self.has_put

