from game_manager import GameManager
from settings import *
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="grid size",
                        type=int, default=DEFAULT_GRID_SIZE)
    parser.add_argument("-d", "--debug", help="debug mode",
                        type=bool, default=DEBUG_MODE)
    parser.add_argument("-f", "--fps", help="frames per second",
                        type=int, default=DEFAULT_FPS)
    args = parser.parse_args()

    gm = GameManager(size=args.size, debug_mode=args.debug, fps=args.fps)
    gm.game_loop()


if __name__ == '__main__':
    main()
