import random
from functools import partial

from .static_map import StaticMap
from .agents import Agents, Player, Package
from .robot import Robot
from .log import log


class World:
    """
    Current state of the world
    includes: StaticMap, Agents
    """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.static_map = None
        self.agents = None
        self.player = None
        self.game_time = 0
        self._agent_map = None

    def init(self, width, height):
        self.width = width
        self.height = height

        self.static_map = StaticMap()
        self.static_map.init(self.width, self.height)

        self.agents = Agents(self)

    @property
    def agent_map(self):
        if self._agent_map is None:
            self._agent_map = [
                [None for x in range(self.width)]
                for y in range(self.height)
            ]
            for agent in self.agents:
                self._agent_map[agent.y][agent.x] = agent
        return self._agent_map

    def add_agent(self, agent):
        self.agents.add_agent(agent)
        self._agent_map = None

    def remove_agent(self, agent):
        self.agents.remove_agent(agent)
        self._agent_map = None

    def agent_move(self, agent, direction, pushed_by=None):
        """
        Move an agent
        Currently does not distinguish much between desired or forced by push!

        :param agent: Agent instance
        :param direction: (int, int)
        :param pushed_by: optional Agent instance which is pushing
        :return: bool
        """
        if not pushed_by:
            agent.dir_x, agent.dir_y = direction

        x, y = self._check_agent_direction(agent, direction)
        if x is None:
            return False

        map_tile = self.static_map.map[y][x]
        if map_tile != StaticMap.Tiles.EMPTY:
            # log(f"{agent} pushed static-map tile {map_tile} at {(x, y)}")
            return False

        other_agent = self.agents.get_agent_at(x, y)
        if other_agent:
            if not other_agent.pushable:
                #if pushed_by:
                #    log(f"{pushed_by} could not push {agent} to {agent.position}")
                return False

            if not self.agent_move(other_agent, direction, pushed_by=agent):
                #if pushed_by:
                #    log(f"{pushed_by} could not push {agent} to {agent.position}")
                return False

        agent.x = x
        agent.y = y

        if not pushed_by:
            agent.last_move_time = self.game_time

        if pushed_by:
            agent.on_pushed(self, pushed_by)
            # log(f"{pushed_by} pushed {agent} to {agent.position}")

        self._agent_map = None
        return True

    def agent_pick(self, agent, direction):
        if agent.is_inventory_full():
            return False

        x, y = self._check_agent_direction(agent, direction)
        if x is None:
            return False

        other_agent = self.agents.get_agent_at(x, y)
        if not other_agent:
            return False

        result = other_agent.on_picked(self, agent)
        if result:
            log(f"{agent} picked {other_agent}")
        return result

    def agent_put(self, agent, direction, item):
        assert item in agent.items, f"Agent {agent} does not have item {item}"
        if item is None:
            return False
        x, y = self._check_agent_direction(agent, direction)
        if x is None:
            return False

        # put into agent
        other_agent = self.agents.get_agent_at(x, y)
        if other_agent:
            if other_agent.on_put(self, agent, item):
                agent.remove_item(item)
                log(f"{agent} put {item} into {other_agent}")
                return True
            # if agent doesn't take, try to push it away
            if not self.agent_move(other_agent, direction, pushed_by=agent):
                return False

        # put onto map
        tile = self.static_map.map[y][x]
        if tile == StaticMap.Tiles.EMPTY:
            agent.remove_item(item)
            item.x, item.y = x, y
            self.add_agent(item)
            log(f"{agent} put {item} at {(x, y)}")
            return True
        return False

    def _check_agent_direction(self, agent, direction):
        assert direction[0] or direction[1], f"Can not move diagonal, got {direction}"
        x = agent.x + direction[0]
        y = agent.y + direction[1]
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return None, None
        return x, y

    def get_empty_position(self, rnd=None):
        if rnd is None:
            rnd = random
        while True:
            x = rnd.randrange(self.width)
            y = rnd.randrange(self.height)
            if self.static_map.map[y][x] != StaticMap.Tiles.EMPTY:
                continue
            if self.agents.get_agent_at(x, y):
                continue
            return x, y

    def can_push_from_to(self, p1, p2):
        """
        Return > 0 if push p1 to p2 is possible
        Returns 0 if it's not possible because
            - p1 -> p2 is not 1 square apart
            - p1 or p2 is out-of-range
            - p1 or p2 is a non-empty tile
            - p2 is no pushable agent
            - the pushable agent can not be pushed because there is no space anywhere behind
                including all further pushable agents
        :param p1: (int, int)
        :param p2: (int, int)
        :return: int
            the number of consecutive pushes that would happen
            e.g. pushing a row of 5 packages would return 5
        """
        if not 0 <= p1[1] < self.height:
            return 0
        if not 0 <= p1[0] < self.width:
            return 0
        if not 0 <= p2[1] < self.height:
            return 0
        if not 0 <= p2[0] < self.width:
            return 0
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        if abs(dx) + abs(dy) != 1:
            return 0
        if self.static_map.map[p2[1]][p2[0]] != StaticMap.Tiles.EMPTY:
            return 0
        if self.static_map.map[p1[1]][p1[0]] != StaticMap.Tiles.EMPTY:
            return 0

        agent = self.agent_map[p2[1]][p2[0]]
        if agent is None:
            return 1
        if not agent.pushable:
            return 0

        succesive_push = self.can_push_from_to(
            p2, (p2[0]+dx, p2[1]+dy)
        )
        if not succesive_push:
            return 0
        return 1 + succesive_push

    def get_way_map(self, exclude_agents=None):
        """
        Return 2d list of booleans determining accessibility
        :param exclude_agents: set of Agent instances which should not be counted
        :return: list, [[bool,..],..]
        """
        way_map = [
            [
                False if tile == StaticMap.Tiles.EMPTY else True
                for tile in row
            ]
            for row in self.static_map.map
        ]
        for agent in self.agents:
            if not exclude_agents or agent not in exclude_agents:
                way_map[agent.y][agent.x] = True
        return way_map

