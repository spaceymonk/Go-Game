import sys
import config


if __name__ == "__main__":
    if config.GAMEMODE == 2:
        from two_player import App
        app = App()
    elif config.GAMEMODE == 1:
        from one_player import App
        app = App()
    app.on_execute()
