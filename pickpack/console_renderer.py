import curses

from .static_map import StaticMap
from .agents import Player, Package, Computer, Shelf
from .items import PickOrder, Article
from .robot import RobotBase


class ConsoleRenderer:

    TILE_MAPPING = {
        StaticMap.Tiles.EMPTY: "  ",
        StaticMap.Tiles.WALL: "[]",
    }

    _instance = None

    def __init__(self, window):
        self.window = window

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_GREEN)

        self.game_window = curses.newpad(10, 60)
        self.stats_window = curses.newpad(10, 50)
        self.stats_window.scrollok(True)
        self.stats_window.idlok(True)
        self.print_window = curses.newpad(10, 50)
        self.print_window.scrollok(True)
        self.print_window.idlok(True)
        self._last_res = ()
        self.__class__._instance = self

    def resolution(self):
        return self.window.getmaxyx()

    def print(self, *args):
        s = " ".join(str(a) for a in args)
        s = self._limit_str_length(s, self.print_window.getmaxyx()[1])
        num_lines = 1 + sum(1 for x in filter(lambda c: c == "\n", s))
        self.print_window.move(0, 0)
        self.print_window.insdelln(num_lines + 1)
        self.print_window.insstr(s)

    def stats(self, *args):
        s = " ".join(str(a) for a in args)
        s = self._limit_str_length(s, self.stats_window.getmaxyx()[1])
        #self.stats_window.clear()
        self.stats_window.move(0, 0)
        self.stats_window.insstr(s)

    def _limit_str_length(self, s, width):
        rs = ""
        line_length = 0
        for c in s:
            if c == "\n" or line_length >= width - 1:
                rs += "\n"
                line_length = 0
            if c != "\n":
                rs += c
                line_length += 1
        return rs

    def render_world(self, world):
        for y in range(world.height):
            for x in range(world.width):
                tile = world.static_map.map[y][x]
                tile_str = self.TILE_MAPPING.get(tile) or str(tile)
                self._draw_game(x, y, tile_str)

        for agent in world.agents:
            self._draw_game(agent.x, agent.y, self._get_agent_str(agent))
            way = getattr(agent, "debug_way", None)
            if way:
                for p in way:
                    self._draw_game_attr(p[0], p[1], curses.color_pair(1))

    def _draw_game(self, x, y, s):
        try:
            self.game_window.addstr(y, x * 2, s)
        except curses.error:
            pass

    def _draw_game_attr(self, x, y, attr):
        try:
            self.game_window.chgat(y, x * 2, 2, attr)
        except curses.error:
            pass

    def _resize(self):
        h, w = self.resolution()
        w3 = w // 3
        self.window.clear()
        self.game_window.resize(h, w3)
        self.print_window.resize(h, w3)
        self.stats_window.resize(h, w3)
        self.game_window.clear()
        self.print_window.clear()
        self.stats_window.clear()

    def _refresh_window(self, window, pos_x):
        ph, pw = window.getmaxyx()
        try:
            window.refresh(
                0, 0,
                0, pos_x,
                ph, pw + pos_x
            )
        except curses.error:
            pass

    def update(self):
        h, w = self.resolution()
        if (h, w) != self._last_res:
            self._last_res = (h, w)
            self._resize()

        _, print_width = self.print_window.getmaxyx()
        _, stats_width = self.stats_window.getmaxyx()
        _, game_width = self.game_window.getmaxyx()

        self._refresh_window(self.stats_window, 0)
        self._refresh_window(self.game_window, stats_width)
        self._refresh_window(self.print_window, w - print_width)

    def _get_agent_str(self, agent):
        if isinstance(agent, Player):
            return "😊"
        elif isinstance(agent, RobotBase):
            return "😎"
        elif isinstance(agent, Computer):
            return "💻"
        elif isinstance(agent, Package):
            return "📦"
        elif isinstance(agent, Shelf):
            return f"{agent.shelf_id}"
        elif isinstance(agent, PickOrder):
            return "✉"
        elif isinstance(agent, Article):
            return "📺"
        return agent.id[:2]



"""
📺 🖨 💾💾⌨ 💿 💻 🔌📞☎ 
🐌🐌⚽ 
🗳
📫 📪 📬 📭 🧾🧾📄📄📖✉
"""