import game.events as events
from game.state import Flag

class EventHandler:
    def __init__(self, io):
        self.io = io
        self.state = io.state

    async def handle_fortify(self):
        valid_commands = ["RECAPITULATE", "SOJOURN", "FORTIFY", "BATTLE", "INDEX"]
        if not self.state.check_flag(Flag.SEEN_FORTIFY_INTRO):
            self.io.print(f"Your [yellow]attributes[/yellow] have been determined based on your allotment. You may review them by [green]recapitulating[/green] (submit the imperative). When you have finished your review, consider [green]sojourn[/green]ing or [green]index[/green]ing. You may also [green]affect[/green] at times, but not now. You are presently [green]fortified[/green] (this also may be submitted at another time) at [blue]{self.state.player.position.name}[/blue].\n")
            self.state.set_flag(Flag.SEEN_FORTIFY_INTRO)

        while True:
            user_input = await self.io.get_input(f"You are currently [green]fortified[/green] at [blue]{self.state.player.position.name}[/blue].")
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

    async def run(self):
        while True:
            if not self.state.check_flag(Flag.SEEN_CHARACTER_CREATION):
                self.io.switch_screen("scene")
                self.state.player = await events.CreateCharacter(self.io).run()
                self.state.player.position = await events.ChooseStartingLocation(self.io).run()
                self.state.set_flag(Flag.SEEN_CHARACTER_CREATION)
                self.io.print("done!")
                self.io.switch_screen("fortify")


            if self.state.screen == "fortify":
                self.handle_fortify()
            elif self.state.screen == "sojourn":
                self.handle_sojourn()
            elif self.state.screen == "battle":
                self.handle_battle()
            else:
                pass

"""
        elif io.screen == "fortify":
            if not io.state.check_flag("seen_fortify_intro"):
                io.print("Your [yellow]attributes[/yellow] have been determined based on your allotment. Submit [green]recapitulate[/green] to review your [yellow]attributes[/yellow]. When you have finished your review, consider [green]sojourn[/green]ing or [green]index[/green]ing. You may also [green]fortify[/green] (though you are already [green]fortified[/green]) and [green]affect[/green].")

            while True:
                user_input = await io.get_input(f"You are currently [green]fortified[/green] at {io.state.player.position}.")
                commands = ["RECAPITULATE", "SOJOURN", "FORTIFY", "BATTLE", "INDEX"]
                if user_input in commands:
                    if user_input == "RECAPITULATE":
                        io.state.player.recapitulate()
                    elif user_input == "INDEX":
                        io.state.player.index()
                    elif user_input == "SOJOURN":
                        io.print("You [green]sojourn[/green].")
                        io.switch_screen("sojourn")
                        break
                    elif user_input == "FORTIFY":
                        io.print("You are already [green]fortified[/green].")
                    elif user_input == "BATTLE":
                        io.print("You begin [green]battling[/green].")
                        io.switch_screen("battle")
                        break
                else:
                    io.print("Improper.")

        elif io.screen == "sojourn":
            io.print("This is the [green]sojourn[/green] screen.")
            while True:
                user_input = await io.get_input("You might want to [green]fortify[/green] or [green]battle[/green].")
                if user_input == "SOJOURN":
                    io.print("You are already [green]sojourning[/green].")
                if user_input == "BATTLE":
                    io.print("You begin to wage war.")
                    io.switch_screen("battle")
                    break
                if user_input == "FORTIFY":
                    io.print("You fortify.")
                    io.switch_screen("fortify")
                    break
                else:
                    io.print("Improper.")

        elif io.screen == "battle":
            io.print("This is the [green]battle[/green] screen.")
            while True:
                user_input = await io.get_input("You might want to [green]sojourn[/green] or [green]fortify[/green].")
                if user_input == "SOJOURN":
                    io.print("You sojourn.")
                    io.switch_screen("sojourn")
                    break
                if user_input == "FORTIFY":
                    io.print("You fortify.")
                    io.switch_screen("fortify")
                    break
                if user_input == "BATTLE":
                    io.print("You are already [green]battling[/green].")
                else:
                    io.print("Improper.")

"""
