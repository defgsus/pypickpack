import unittest

from pickpack.astar import astar_search

MAP1 = [
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 0],
]

MAP2 = [
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
]


def adjacent_nodes_func_for_map(map):
    def _func(pos):
        ret_nodes = []
        for dx, dy in (
                (-1, 0),
                (0, -1),
                (1, 0),
                (0, 1),
        ):
            p = (pos[0] + dx, pos[1] + dy)
            if not 0 <= p[0] < len(map[0]) or not 0 <= p[1] < len(map):
                continue
            if map[p[1]][p[0]]:
                continue

            ret_nodes.append((p, 1))
        return ret_nodes
    return _func


class TestAStar(unittest.TestCase):

    def test_100_astar_map1(self):
        path = astar_search(
            (0, 3), (3, 0),
            adjacent_nodes_func=adjacent_nodes_func_for_map(MAP1)
        )
        self.assertEqual(
            [(0, 3), (0, 2), (0, 1), (1, 1), (2, 1), (3, 1), (3, 0)],
            path
        )

    def test_101_astar_map2(self):
        path = astar_search(
            (0, 0), (2, 3),
            adjacent_nodes_func=adjacent_nodes_func_for_map(MAP2)
        )
        self.assertEqual(
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)],
            path
        )

