async def fortify_logic(io):
    io.print("This is the [green]fortify[/green] screen.")
    while True:
        user_input = await io.get_input("You might want to [green]sojourn[/green] or [green]battle[/green].")
        if user_input == "SOJOURN":
            io.print("You sojourn.")
            io.push_screen("sojourn")
            break
        if user_input == "BATTLE":
            io.print("You begin to wage war.")
            io.push_screen("battle")
            break
        if user_input == "FORTIFY":
            io.print("You are already [green]fortified[/green].")
        else:
            io.print("Improper.")
