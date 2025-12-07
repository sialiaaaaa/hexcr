import game.events as events

class Player:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.position = "home"

class GameState:
    def __init__(self):
        self.player = None
        self.screen = None
        self.flags = []

    def check_flag(self, flag):
        if flag in self.flags:
            return True
        else:
            return False
