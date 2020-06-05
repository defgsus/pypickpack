import random

from .static_map import StaticMap
from .agents import Player, Package, Computer, Shelf
from .robot import Robot, RandomRobot


def init_random_world(world, width, height, rnd=None):
    if rnd is None:
        rnd = random

    world.init(width, height)

    _make_static_border(world)

    # random walls
    for i in range(world.width * world.height // 50):
        x = rnd.randrange(world.width)
        y = rnd.randrange(world.height)
        world.static_map.map[y][x] = StaticMap.Tiles.WALL

    # packages
    for i in range(world.width * world.height // 5):
        p = Package(f"PK{i}")
        p.x, p.y = world.get_empty_position(rnd=rnd)
        world.agents.add_agent(p)

    # robots
    for i in range(1):
        robot = Robot(f"R{i}")
        robot.x, robot.y = world.get_empty_position(rnd=rnd)
        world.agents.add_agent(robot)

    _create_random_player(world, rnd)


def _make_static_border(world):
    for x in range(world.width):
        world.static_map.map[0][x] = StaticMap.Tiles.WALL
        world.static_map.map[world.height-1][x] = StaticMap.Tiles.WALL

    for y in range(world.height):
        world.static_map.map[y][0] = StaticMap.Tiles.WALL
        world.static_map.map[y][world.width-1] = StaticMap.Tiles.WALL


def _create_random_player(world, rnd):
    world.player = Player("player")
    world.player.x, world.player.y = world.get_empty_position(rnd=rnd)

    world.agents.add_agent(world.player)



def init_pickpack_world(world):
    class Things:
        W = 1   # wall
        P = 10  # player
        R = 11  # robot
        C = 20  # computer
        S = 30  # shelf

    MAP = """
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
W                   WCWW     W
W   P                  W     W
W                      W     W
W                            W
W                      WWWWWWW
W                            W
W                            W
W                            W
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W                            W
W                            W
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W   WW  WW  WW  WW  WW  WW   W                 
W   SS  SS  SS  SS  SS  SS   W                
W                            W
W                            W
WR                          RW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
"""
    MAP = [
        [getattr(Things, c) if c != " " else 0 for c in line]
        for line in MAP.splitlines()
        if line.strip()
    ]

    world.init(len(MAP[0]), len(MAP))

    shelf_counter = 0
    for y in range(world.height):
        for x in range(world.width):
            m = MAP[y][x]

            if m == Things.W:
                world.static_map.map[y][x] = StaticMap.Tiles.WALL

            elif m == Things.R:
                agent = Robot(f"R{len(world.agents)}")
                agent.x, agent.y = x, y
                world.agents.add_agent(agent)

            elif m == Things.C:
                agent = Computer(f"CO{len(world.agents)}")
                agent.x, agent.y = x, y
                world.agents.add_agent(agent)

            elif m == Things.S:
                agent = Shelf(chr(ord('A') + shelf_counter // 9) + chr(ord('1') + shelf_counter % 9))
                agent.x, agent.y = x, y
                world.agents.add_agent(agent)
                shelf_counter += 1

            elif m == Things.P:
                agent = Player(f"Player")
                agent.x, agent.y = x, y
                world.agents.add_agent(agent)
                world.player = agent
