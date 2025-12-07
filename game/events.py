from game.state import Player

class Event:
    def __init__(self, io):
        self.io = io
        self.state = io.state

    async def run(self):
        raise NotImplementedError

class CreateCharacter(Event):
    async def run(self):
        while True:
            name = await self.io.get_input("In parts beyond they have called you by many names. Here you will be known as...")
            if name:
                self.io.print(f"Your name is [red]{name}[/red].")
                break
            else:
                self.io.print("Why do you falter?")

        statistics = 10

        return Player(name, statistics)


