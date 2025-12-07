import game.events as events

async def scene_logic(io):
    if io.state.flags["need_character_creation"]:
        io.state.player = await events.CreateCharacter(io).run()
        io.state.flags["need_character_creation"] = False
    io.print(f"Your name is [red]{io.state.player.name}[/red].")
    io.switch_screen("fortify")

async def fortify_logic(io):
    io.print("")
    io.print("This is the [green]fortify[/green] screen.")
    while True:
        user_input = await io.get_input("You might want to [green]sojourn[/green] or [green]battle[/green].")
        if user_input == "SOJOURN":
            io.print("You sojourn.")
            io.switch_screen("sojourn")
            break
        if user_input == "BATTLE":
            io.print("You begin to wage war.")
            io.switch_screen("battle")
            break
        if user_input == "FORTIFY":
            io.print("You are already [green]fortified[/green].")
        else:
            io.print("Improper.")

async def sojourn_logic(io):
    io.print("")
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

async def battle_logic(io):
    io.print("")
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
