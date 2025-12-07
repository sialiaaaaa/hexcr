import game.events as events

class EventHandler:
    def __init__(self, io):
        self.io = io
        self.state = io.state

    async def run(self):
        if not self.state.check_flag("seen_character_creation"):
            self.io.switch_screen("scene")
            self.state.player = await events.CreateCharacter(self.io).run()
            self.state.flags.append("seen_character_creation")

        self.io.switch_screen("fortify")
        if not self.state.check_flag("seen_fortify_intro"):
            self.io.print("Your [yellow]attributes[/yellow] have been determined based on your allotment. Submit [green]recapitulate[/green] to review your [yellow]attributes[/yellow]. When you have finished your review, consider [green]sojourn[/green]ing or [green]index[/green]ing. You may also [green]fortify[/green] (though you are already [green]fortified[/green]) and [green]affect[/green].")
            self.state.flags.append("seen_fortify_intro")

        while True:
            user_input = await self.io.get_input(f"You are currently fortified at {self.state.player.position}.")
            commands = ["RECAPITULATE", "SOJOURN", "FORTIFY", "BATTLE", "INDEX"]
            if user_input in commands:
                if user_input == "RECAPITULATE":
                    self.state.player.recapitulate()
                elif user_input == "INDEX":
                    self.state.player.index()
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
