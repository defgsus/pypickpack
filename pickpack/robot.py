import random

from .agents import AgentBase
from .pos import direction_int
from .astar import astar_search
from .log import log
from .static_map import StaticMap


class RobotBase(AgentBase):

    def __init__(self, id, processing_fps=3):
        super().__init__(id, processing_fps=processing_fps)

    def is_next_move_frame(self, world):
        return True


class RandomRobot(RobotBase):

    def __init__(self, id):
        super().__init__(id)

    def process(self, world, time_delta):
        if self.is_next_move_frame(world):
            if random.randrange(10) == 0:
                self.dir_x, self.dir_y = random.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))

            if not world.agent_move(self, self.direction):
                self.dir_x, self.dir_y = random.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))


class Robot(RobotBase):

    def __init__(self, id):
        super().__init__(id)

    def process(self, world, time_delta):
        if self.is_next_move_frame(world):

            way_to_player = astar_search(
                self.position, world.player.position,
                lambda pos: self.get_adjacent_nodes(world, pos, exclude_agents={self})
            )

            self.debug_way = None
            if way_to_player:
                next_pos = way_to_player[1]
                dirx, diry = direction_int(self.position, next_pos)
                if dirx or diry:
                    world.agent_move(self, (dirx, diry))

                self.debug_way = way_to_player

    def get_adjacent_nodes(self, world, pos, exclude_agents=None):
        """
        Returns the accessible adjacent nodes in the world and their cost
        :param world: World
        :param pos: (int, int)
        :return: list of ((int, int), float)
        """
        ret_nodes = []
        for dx, dy in (
                (-1, 0),
                (0, -1),
                (1, 0),
                (0, 1),
        ):
            p = (pos[0] + dx, pos[1] + dy)
            if not 0 <= p[0] < world.width or not 0 <= p[1] < world.height:
                continue
            tile = world.static_map.map[p[1]][p[0]]
            if tile != StaticMap.Tiles.EMPTY:
                continue

            cost = 1.

            agent = world.agent_map[p[1]][p[0]]
            if agent:
                if not exclude_agents or agent not in exclude_agents:
                    if not agent.pushable:
                        continue
                    can_push = world.can_push_from_to(p, (p[0] + dx, p[1] + dy))
                    if not can_push:
                        continue
                    cost = 2. + can_push

            ret_nodes.append((p, cost))

        return ret_nodes
