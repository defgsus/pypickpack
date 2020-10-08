import time

from .world import World
from .agents import Player
from .robots import RobotBase
from .log import log


class Game:

    """
    Container that helps 'playing' a World
    and process all automatic agents
    """

    def __init__(self):
        self.world = World()
        self._last_proc_time = 0
        self.game_time = 0
        self.pause = False

    def process_key(self, key):
        if key == "KEY_UP":
            self.world.agent_move(self.world.player, (0, -1))
        elif key == "KEY_DOWN":
            self.world.agent_move(self.world.player, (0, 1))
        elif key == "KEY_LEFT":
            self.world.agent_move(self.world.player, (-1, 0))
        elif key == "KEY_RIGHT":
            self.world.agent_move(self.world.player, (1, 0))
        elif key == "q":
            item = self.world.player.selected_item()
            if item:
                self.world.agent_put(
                    self.world.player, self.world.player.direction, item
                )
        elif key == "a":
            self.world.agent_pick(self.world.player, self.world.player.direction)
        elif key and ord('1') <= ord(key[0]) <= ord('9'):
            self.world.player.selected_item_index = ord(key[0]) - ord('1')
        elif key == "p":
            self.pause = not self.pause

    def process_game(self):
        cur_time = time.time()
        time_delta = min(1., cur_time - self._last_proc_time)
        self._last_proc_time = cur_time

        if self.pause:
            return

        self.world.game_time = self.game_time

        for agent in self.world.agents:
            if agent.processing_fps:
                if (self.world.game_time - agent._last_processing_time) * agent.processing_fps >= 1.:
                    agent.process(self.world, time_delta)
                    agent._last_processing_time = self.world.game_time

        self.game_time += time_delta

    def get_stats_str(self):
        s = "use: up,down,left,right: move\n"
        s += "q: put, a: pick, p: play/pause\n"

        s += f"\ntime: {round(self.game_time, 2)} sec\n\n"

        s += self.get_agents_stats_str(self.world.player)
        for agent in self.world.agents:
            if isinstance(agent, RobotBase):
                s += "\n" + self.get_agents_stats_str(agent)
        s += "\n"

        return s

    def get_agents_stats_str(self, agent):
        s = f"{agent.stats_str()}\n"
        s += "items: " + ", ".join(str(i) for i in agent.items) + "\n"
        if isinstance(agent, Player):
            s += f"selected item: {agent.selected_item()} ({agent.selected_item_index+1})\n"
        return s


