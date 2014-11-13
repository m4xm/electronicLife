from lib.WindowManager import WindowManager
from lib.Window import Window, OptionPane
from lib.MapManager import MapManager
import curses
from time import sleep, time


class EvolutronicLife(object):

    def __init__(self, map_filename):
        self._win_manager = WindowManager()
        self._map_manager = MapManager(map_filename)

    def run(self):
        """
        the main game loop + some initial configurations
        """

        self._win_manager.init_curses()

        self._win_manager["info_win"] = Window(1, 140, 0, 0)
        self._win_manager["game_win"] = Window(35, 140, 1, 0)
        self._win_manager["option_pane"] = OptionPane(["Pause", "Faster", "Slower", "Exit"], 140, 36, 0)

        start_time = time()
        sec_per_step = 0.5
        step = 0
        keep_running = True
        while keep_running:
            step += 1
            start = time()

            self._win_manager.clear()

            self._win_manager["info_win"].curses_window.addstr(0, 0,
                                                               "{:5s} {:5.1f}".format('time:', round(time() - start_time, 1))
                                                               + "{:13s} {:4.1f}".format(' steps per s:', round(1 / sec_per_step, 1))
                                                               + "{:4s} {:4d}".format(' step:', step))

            self._map_manager.update()
            self._map_manager.draw_map(self._win_manager["game_win"].curses_window)

            self._win_manager.update()

            c = self._win_manager.main_win.getch()

            if c == 265:
                while True:
                    c = self._win_manager.main_win.getch()
                    if c == 265:
                        break
                    if c == 268:
                        keep_running = False
            if c == 266:
                sec_per_step = round(sec_per_step - 0.1, 1)
                if sec_per_step <= 0:
                    sec_per_step = 0.1
            if c == 267:
                sec_per_step = round(sec_per_step + 0.1, 1)
                if sec_per_step > 2:
                    sec_per_step = 2
            if c == 268:
                keep_running = False

            if time() - start < sec_per_step:
                sleep(sec_per_step - (time() - start))

        self._win_manager.deinit_curses()

        return 0