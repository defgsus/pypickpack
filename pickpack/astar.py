
from .pos import distance, manhatten_distance, direction


def astar_search(start_node, end_node, adjacent_nodes_func, goal_cost_func=None):
    """
    Get optimal path between start_node and end_node
    :param start_node: (int, int)
    :param end_node: (int, int)
    :param adjacent_nodes_func: function((int, int))
        function returning all accessible adjacent nodes in the world and their cost
        as list of ((int, int), float)
    :param goal_cost_func: function((int, int), (int, int))
        function returning heuristic cost between two positions
        Since this game is only up/down/left/right, it defaults to "manhatten" distance
    :return: list of (int, int) or None
    """
    if goal_cost_func is None:
        goal_cost_func = lambda p1, p2: manhatten_distance(p1, p2)

    infinity = 2 << 31

    closed_set = set()
    open_set = {start_node}

    # cost of getting from start to this node
    g_score = {start_node: 0}

    # total cost if getting from start to end, through this node
    f_score = {end_node: goal_cost_func(start_node, end_node)}

    came_from = dict()

    while open_set:
        # pick smallest f from open_set
        current_node = None
        min_score = infinity
        for n in open_set:
            f = f_score.get(n, infinity)
            if f < min_score or current_node is None:
                min_score, current_node = f, n
        open_set.remove(current_node)

        # found!
        if current_node == end_node:
            path = [current_node]
            while current_node in came_from:
                current_node = came_from[current_node]
                path.append(current_node)
            return list(reversed(path))

        # flag as evaluated
        closed_set.add(current_node)

        for neighbor_node, step_cost in adjacent_nodes_func(current_node):

            if neighbor_node in closed_set:
                continue

            if neighbor_node not in open_set:
                open_set.add(neighbor_node)

            g = g_score.get(current_node) + step_cost
            # prune this path
            if g >= g_score.get(neighbor_node, infinity):
                continue

            # continue this path
            came_from[neighbor_node] = current_node
            g_score[neighbor_node] = g
            f_score[neighbor_node] = g + goal_cost_func(neighbor_node, end_node)

    return None



