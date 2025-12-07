from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import RichLog, Input, Placeholder, Static
from textual.containers import Container, Vertical, Horizontal

from asyncio import Event
import re

pattern = re.compile('[\\W_]+')

from game.screens import EventHandler

"""
Shared input/output class so other functions can interface with Textual
"""
class GameIO:
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

    @property
    def state(self):
        return self.app.game_state

    def print(self, message):
        """Searches for a RichLog tagged 'output' on the current screen and displays text there."""
        log = self.app.battle_log
        log.write(message)

    async def get_input(self, prompt: str):
        """Find a RichLog as above and show text there, then store user input."""
        return await self.screen.get_input(prompt)

    def push_screen(self, screen_name: str):
        """Push a screen by name."""
        self.app.push_screen(screen_name)

    def pop_screen(self):
        self.app.pop_screen()

    def switch_screen(self, target_screen_name: str):
        self.app.switch_screen(target_screen_name)



"""Various widgets for use across various screens."""
class InputField(Input):
    def __init__(self, id):
        super().__init__()
        self.placeholder = "Supply input..."
        self.id = id

class BattleLog(RichLog):
    can_focus = False

class BattleLogContainer(Container):
    """Placeholder that will hold the battle log"""
    pass

"""Basic Screen from which to inherit."""
class GameScreen(Screen):
    def __init__(self):
        super().__init__()
        self.input_value = None
        self.input_event = Event()

    def on_mount(self):
        pass

    def on_screen_resume(self):
        """Called when returning to this screen after it was suspended"""
        self.run_worker(self._relocate_battle_log())

    async def _relocate_battle_log(self):
        """Move the battle_log to this screen's placeholder"""
        try:
            container = self.query_one(BattleLogContainer)
            battle_log = self.app.battle_log

            # Remove from current parent if it has one
            if battle_log.parent is not None:
                await battle_log.remove()

            # Mount to new container
            await container.mount(battle_log)
        except Exception as e:
            self.log(f"Error relocating battle log: {e}")

    def compose(self):
        yield BattleLogContainer()
        yield InputField(id="input")

    async def get_input(self, prompt: str) -> str:
        """Internal method to handle input collection"""
        self.app.battle_log.write(prompt)
        self.input_event.clear()
        await self.input_event.wait()
        return pattern.sub('', self.input_value).upper()

    def on_input_submitted(self, event: Input.Submitted):
        """Handle when user submits input"""
        self.app.battle_log.write(f"> {pattern.sub('', event.value).upper()}\n")
        self.input_value = event.value
        self.input_event.set()
        event.input.clear()


"""Screens."""

class SceneScreen(GameScreen):
    pass

class FortifyScreen(GameScreen):
    pass

class SojournScreen(GameScreen):
    def compose(self):
        with Horizontal():
            with Vertical(id="sojourn-left-panel"):
                yield Placeholder(label="top left")
                yield BattleLogContainer()
            yield Placeholder(label="right")
        yield InputField(id="input")

class BattleScreen(GameScreen):
    def compose(self):
        with Vertical():
            with Horizontal(id="battle-top-panel"):
                yield Placeholder(label="friends")
                yield Placeholder(label="foes")
            yield BattleLogContainer()
        yield InputField(id="input")

class Game(App):

    SCREENS = { "scene": SceneScreen, "fortify": FortifyScreen, "sojourn": SojournScreen, "battle": BattleScreen }

    CSS_PATH = "../styles.css"

    def __init__(self, game_state):
        super().__init__()
        self.battle_log = BattleLog(id="battle-log", wrap=True, markup=True)
        self.game_state = game_state

    def on_mount(self):
        self.push_screen("scene")

        # Create IO interface with access to both screen and app
        self.io = GameIO(self, self.app)
        self.event_handler = EventHandler(self.io)

        self.run_worker(self._run_game())

    async def _run_game(self):
        io = GameIO(self.screen, self)
        event_handler = EventHandler(io)
        await event_handler.run()

