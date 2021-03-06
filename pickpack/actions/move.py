from .base import ActionBase
from .._2d import distance, manhatten_distance, direction_int
from ..astar import astar_search


class MoveBefore(ActionBase):

    def __init__(self, position):
        super().__init__(position=position)

    def get_estimated_cost(self, world, agent):
        mdist = manhatten_distance(agent.position, self.parameters["position"])
        return max(0, mdist-1)

    def is_finished(self, world, agent):
        return manhatten_distance(agent.position, self.parameters["position"]) == 1

    def execute(self, world, agent):
        if manhatten_distance(agent.position, self.parameters["position"]) == 1:
            return True

        goal_node = world.get_empty_neighbour(self.parameters["position"], close_to=agent.position)
        if not goal_node:
            return False

        path = astar_search(
            start_node=agent.position,
            end_node=goal_node,
            adjacent_nodes_func=lambda pos: agent.get_adjacent_nodes(world, pos, exclude_agents={agent})
        )
        agent.debug_way = path
        if not path:
            return False

        next_pos = path[1]
        dirx, diry = direction_int(agent.position, next_pos)
        if dirx or diry:
            world.agent_move(agent, (dirx, diry))
            return True

        return False


class MoveTo(ActionBase):

    def __init__(self, position):
        super().__init__(position=position)

    def get_estimated_cost(self, world, agent):
        mdist = manhatten_distance(agent.position, self.parameters["position"])
        return max(0, mdist-1)

    def is_finished(self, world, agent):
        return agent.position == self.parameters["position"]

    def execute(self, world, agent):
        if agent.position == self.parameters["position"]:
            return True

        path = astar_search(
            start_node=agent.position,
            end_node=self.parameters["position"],
            adjacent_nodes_func=lambda pos: agent.get_adjacent_nodes(world, pos, exclude_agents={agent})
        )
        agent.debug_way = path
        if not path:
            return False

        next_pos = path[1]
        dirx, diry = direction_int(agent.position, next_pos)
        if dirx or diry:
            world.agent_move(agent, (dirx, diry))
            return True

        return False
