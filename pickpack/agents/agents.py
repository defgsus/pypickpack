from .base import AgentBase

from ..log import log
from .._2d import *


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

