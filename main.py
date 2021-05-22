import sys
from app import App
import config


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
"""
Usage: python main.py [gamemode] [boardsize]
    gamemode    Select below values:
                "0" - player-player
                "1x" - player-computer, "x" specifies player's stone:
                    b - player will use black stones
                    w - player will use white stones
                "2" - computer-computer
    boardsize   Specify as "13x13" or "19x19"
Example usages:
python main.py 0 13x13
python main.py 1b 19x19

This program written by Berktug Kaan Ozkan.
GitHub: https://github.com/spaceymonk
""")
        sys.exit(1)
    app = App()
    app.on_execute()
