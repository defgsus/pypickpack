from .._2d import distance, manhatten_distance, direction_int
from ..astar import astar_search


class ActionBase:

    def __init__(self, **parameters):
        self.parameters = parameters

    def __repr__(self):
        return f"{self.__class__.__name__}({self.parameters})"

    def copy(self):
        return self.__class__(**self.parameters)

    def is_finished(self, world, agent):
        raise NotImplementedError

    def execute(self, world, agent):
        """
        Let agent execute the action in world.
        :param world: World
        :param agent: AgentBase
        :return: bool, If it could be executed or is already finished
        """
        raise NotImplementedError

    def get_estimated_cost(self, world, agent):
        """
        Return an estimated cost of executing this action through agent in world
        :param world: World
        :param agent: AgentBase
        :return: int/float
        """
        raise NotImplementedError
