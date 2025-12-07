import game.events as events

class GameState:
    def __init__(self, next_event):
        self.next_event = next_event
        self.player = None
        self.name = "test"
