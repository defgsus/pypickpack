import curses
import time

from pickpack.game import Game
from pickpack.console_renderer import ConsoleRenderer
from pickpack.world_init import init_random_world, init_pickpack_world


def main(window):
    curses.curs_set(0)
    window.nodelay(True)
    window.clear()

    renderer = ConsoleRenderer(window)
    renderer.print("Welcome to pickpack!")

    game = Game()
    #init_random_world(game.world, 30, 50)
    init_pickpack_world(game.world)

    try:
        while True:
            try:
                key = window.getkey()
                #renderer.print("KEY", key)
                game.process_key(key)
            except curses.error:
                pass

            renderer.render_world(game.world)
            renderer.stats(game.stats_str())
            renderer.update()

            game.process_game()
            time.sleep(1 / 30)

    except KeyboardInterrupt:
        pass


def debug():
    from pickpack.astar import AStar
    game = Game()

    game.process_game()


if __name__ == "__main__":
    curses.wrapper(main)
    #debug()