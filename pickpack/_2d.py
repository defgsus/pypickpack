"""
Some helper for 2d positions as tuples
"""
import math


def add_2d(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def distance(p1, p2):
    dx, dy = p1[0] - p2[0], p1[1] - p2[1]
    return math.sqrt(dx*dx + dy*dy)


def manhatten_distance(p1, p2):
    dx, dy = p1[0] - p2[0], p1[1] - p2[1]
    return abs(dx) + abs(dy)


def direction(p1, p2, normalized=True):
    dx, dy = p1[0] - p2[0], p1[1] - p2[1]
    if normalized:
        d = math.sqrt(dx*dx + dy*dy)
        dx, dy = dx/d, dy/d
    return dx, dy


def direction_int(p1, p2):
    dx = p2[0] - p1[0]
    if dx > 0:
        return 1, 0
    if dx < 0:
        return -1, 0
    dy = p2[1] - p1[1]
    if dy > 0:
        return 0, 1
    if dy < 0:
        return 0, -1
    return 0, 0




