import game.events as events

class Player:
    def __init__(self, name, statistics):
        self.name = name
        self.statistics = statistics

class GameState:
    def __init__(self):
        self.player = None
        self.flags = {"need_character_creation": True}
