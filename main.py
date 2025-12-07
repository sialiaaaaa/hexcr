from ui.app import Game
from game.state import GameState
import game.events as events
"""
A main file calls a `ui.py` that runs Textual. The UI has three screens, which can each recieve input and be given output. For example, one screen will have a RichLog that might display text, and an Input that will receive input. Even though Textual will be running a loop, interacting with this screen should feel just like using a terminal, displaying synchronous output and waiting for input. Another screen might show more complicated information, but should still be able to receive input, send it out to other modules, and be returned output by those modules. Also, certain screens need to be able to share the same RichLog or other elements. Then, in those "other modules" I mentioned, I should simply be able to write straightforward Python that can easily `print` to or assign variables to input from the Textual app.
"""
def main():
    print("Initialising game...")
    state = GameState(next_event=events.CharacterCreation)
    print("Starting Textual app...")
    app = Game(state)
    app.run()


if __name__ == "__main__":
    main()
