import game.events as events
from game.state import Flag
from game.shared import inflector, gen
import humanize

class EventHandler:
    def __init__(self, io):
        self.io = io
        self.state = io.state

    async def handle_fortify(self):
        valid_commands = ["RECAPITULATE", "SOJOURN", "FORTIFY", "BATTLE", "INDEX"]
        if not self.state.check_flag(Flag.SEEN_FORTIFY_INTRO):
            self.io.print(f"Your [yellow]attributes[/yellow] have been determined based on your allotment. You may review them by [green]recapitulating[/green] (submit the imperative). When you have finished your review, consider [green]sojourn[/green]ing or [green]index[/green]ing. You may also [green]affect[/green] at times, but not now. You are presently [green]fortified[/green] (this also may be submitted at another time) at [blue]{inflector.an(self.state.player.position.name)}[/blue].\n")
            self.state.set_flag(Flag.SEEN_FORTIFY_INTRO)

        while True:
            user_input = await self.io.get_input(f"You are currently [green]fortified[/green] at [blue]{inflector.an(self.state.player.position.name)}[/blue].")
            commands = ["RECAPITULATE", "SOJOURN", "FORTIFY", "BATTLE", "INDEX"]
            if user_input in commands:
                if user_input == "RECAPITULATE":
                    self.io.print(self.state.player.recapitulate())
                elif user_input == "INDEX":
                    self.io.print(f"You bear {self.state.player.index()}.")
                elif user_input == "SOJOURN":
                    self.io.print("You [green]sojourn[/green].")
                    self.io.switch_screen("sojourn")
                    break
                elif user_input == "FORTIFY":
                    self.io.print("You are already [green]fortified[/green].")
                elif user_input == "BATTLE":
                    self.io.print("You begin [green]battling[/green].")
                    self.io.switch_screen("battle")
                    break
            else:
                self.io.print("Improper.")

    async def handle_sojourn(self):
        locations = []
        for i in range(30):
            locations.append(gen.generate_random({"place"}))
        self.io.print(f"You may sojourn to {humanize.natural_list([inflector.an(location.name) for location in locations])}.")
        self.io.switch_screen("fortify")

    async def run(self):
        while True:
            if not self.state.check_flag(Flag.SEEN_CHARACTER_CREATION):
                self.io.switch_screen("scene")
                self.state.player = await events.CreateCharacter(self.io).run()
                self.state.player.position = await events.ChooseStartingLocation(self.io).run()
                for i in range(3):
                    self.state.player.inventory.append(gen.generate_random({"object"}))
                self.io.print("You have been provided with a small selection of [blue]possessions[/blue].")
                self.state.set_flag(Flag.SEEN_CHARACTER_CREATION)
                self.io.switch_screen("fortify")


            if self.state.screen == "fortify":
                await self.handle_fortify()
            elif self.state.screen == "sojourn":
                await self.handle_sojourn()
            elif self.state.screen == "battle":
                await self.handle_battle()
            else:
                pass

