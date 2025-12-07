def write_some_prompts(screen):
    while True:
        user_input = await screen.get_input("Type [green]sojourn[/green] to change screens.")
        if user_input == "SOJOURN":
            screen.print(f"You said {user_input}.")
            # Switch screens somehow? Need to be able to write app.push_screen here, but I can only see the screen rather than the app from this function.
            break
        else:
            screen.print(f"You said {user_input}, which is wrong.")
