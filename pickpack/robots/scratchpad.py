import random

from .base import RobotBase
from .._2d import direction_int
from ..astar import astar_search
from ..log import log
from ..static_map import StaticMap


class RandomRobot(RobotBase):

    def __init__(self, id):
        super().__init__(id)

    def process(self, world, time_delta):
        if self.is_next_move_frame(world):
            if random.randrange(10) == 0:
                self.dir_x, self.dir_y = random.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))

            if not world.agent_move(self, self.direction):
                self.dir_x, self.dir_y = random.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))


class RobotFollowPlayer(RobotBase):

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


class Robot(RobotBase):

    def __init__(self, id):
        super().__init__(id)

    def process(self, world, time_delta):
        from ..actions import MoveTo, MoveBefore
        from ..agents import Package, Shelf

        possible_actions = [
            MoveBefore(world.player.position),
        ]

        for klass in (Package, Shelf):
            agent = world.get_closest_agent(self.position, klass)
            if agent:
                possible_actions.append(MoveBefore(agent.position))

        # log(possible_actions)

        possible_actions[1].execute(world, self)


