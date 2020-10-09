import random

from .base import RobotBase
from .._2d import direction_int
from ..astar import astar_search
from ..log import log
from ..static_map import StaticMap
from ..items import Article, PickOrder


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
        self.performance = 0

    def copy(self):
        c = super().copy()
        c.performance = self.performance
        return c

    def on_has_put(self, item, position=None, other_agent=None):
        from ..agents import Package
        from ..items import Article
        if isinstance(item, Article):
            if isinstance(other_agent, Package):
                self.performance += 1

    def process(self, world, time_delta):
        possible_actions = self.get_possible_actions(world)

        evaluated_actions = self.evaluate_actions(world, possible_actions)

        #possible_actions.sort(key=lambda action: action.get_estimated_cost(world, self))

        #log(possible_actions)
        #log(evaluated_actions)

        if evaluated_actions:
            log(evaluated_actions[0])
            action = evaluated_actions[0]["action"]
            #action = random.choice(possible_actions)
            action.execute(world, self)

    def get_possible_actions(self, world):
        from ..actions import MoveTo, MoveBefore, PickDirection, PutDirection
        from ..agents import Player, Package, Shelf, Computer
        from ..items import Article, PickOrder

        classes_to_approach = (Computer, PickOrder, Player, Robot, Package, Shelf, Article)

        possible_actions = [
            # MoveBefore(world.player.position),
            PickDirection((-1, 0)),
            PickDirection((1, 0)),
            PickDirection((0, -1)),
            PickDirection((0, 1)),
        ]
        for item in self.items:
            possible_actions += [
                PutDirection((-1, 0), item.id),
                PutDirection((1, 0), item.id),
                PutDirection((0, -1), item.id),
                PutDirection((0, 1), item.id),
            ]

        for klass in classes_to_approach:
            agent = world.get_closest_agent(self.position, klass, exclude_agents=[self])
            if agent:
                possible_actions.append(MoveBefore(agent.position))

        return possible_actions

    def evaluate_actions(self, world, actions):
        ret_actions = []

        for action in actions:
            value = self._evaluate_action(world, action, depth=1)
            if value is not None:
                ret_actions.append({
                    "action": action,
                    "value": value,
                })

        ret_actions.sort(key=lambda a: -a["value"])
        return ret_actions

    def _evaluate_action(self, world, action, depth):
        action = action.copy()
        world_copy = world.copy()
        self_copy = world_copy.agents.get_by_id(self.id)

        action_passed = False
        for i in range(100):
            if not action.execute(world_copy, self_copy):
                break
            if action.is_finished(world_copy, self_copy):
                action_passed = True
                break

        if not action_passed:
            return

        cur_value = self_copy.get_heuristic_value(world_copy)
        if depth < 1:
            return cur_value

        best_action, best_value = None, None
        new_actions = self_copy.get_possible_actions(world_copy)
        for new_action in new_actions:
            value = self._evaluate_action(world_copy, new_action, depth - 1)
            if value is not None:
                if best_value is None or value > best_value:
                    best_action, best_value = new_action, value

        return max(best_value, cur_value) if best_value is not None else cur_value

    def get_heuristic_value(self, world):
        value = 0

        value += min(0, self.max_items - len(self.items) * 4)

        value += len(self.items_by_class(Article)) * 2
        value += len(self.items_by_class(PickOrder)) * 3

        value += self.performance * 5

        return value
