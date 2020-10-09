from .base import AgentBase

from ..log import log
from .._2d import *


class Agents:

    def __init__(self):
        self.agents = []

    def __iter__(self):
        return iter(self.agents)

    def __len__(self):
        return len(self.agents)

    def __getitem__(self, i):
        return self.agents[i]

    def copy(self):
        c = self.__class__()
        c.agents = [a.copy() for a in self.agents]
        return c

    def add_agent(self, agent):
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
        ret = self.__class__()
        ret.agents = list(filter(
            lambda a: isinstance(a, classes),
            self.agents
        ))
        return ret

    def get_by_id(self, id):
        for a in self.agents:
            if a.id == id:
                return a
