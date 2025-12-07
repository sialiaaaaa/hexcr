class Event:
    def __init__(self, io):
        self.io = io

    def run(self):
        raise NotImplementedError("Events must contain their own run logic.")

class CharacterCreation(Event):
    def run(self):
        self.io.print(f"I'm the run function of a character creation event. The name of the state is {self.io.state.name}")

        name = self.io.get_input("test") # needs to behave like they do in screens.py, but can't be async

