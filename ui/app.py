from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import RichLog, Input, Placeholder
from textual.containers import Container

from asyncio import Event
import re

pattern = re.compile('[\\W_]+')

import game.sample_logic as sample_logic

"""
Shared input/output class so other functions can interface with Textual
"""
class GameIO:
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

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
        self.app.pop_screen()
        self.app.push_screen(target_screen_name)

"""Various widgets for use across various screens."""
class InputField(Input):
    DEFAULT_CSS = "InputField { dock: bottom; border: aliceblue; }"

class BattleLog(RichLog):
    can_focus = False
    DEFAULT_CSS = "BattleLog { height: 1fr; border: aliceblue; }"

"""Basic Screen from which to inherit."""
class GameScreen(Screen):
    def __init__(self):
        super().__init__()
        self.input_value = None
        self.input_event = Event()
        self.io = None  # Will be set when mounted
        self.log_container_id = "log-container"

    def on_mount(self):
        container = self.query_one(f"#{self.log_container_id}", Container)
        container.mount(self.app.battle_log)

        # Create IO interface with access to both screen and app
        self.io = GameIO(self, self.app)
        self.run_worker(self.main_flow())

    def compose(self):
        yield Container(id=self.log_container_id)
        yield InputField(id="input", placeholder="Enter command...")

    async def on_unmount(self):
        # Remove battle log from this screen (but don't delete it)
        # It will be preserved and can be mounted in the next screen
        if self.app.battle_log in self.query(BattleLog):
            await self.app.battle_log.remove()

    async def get_input(self, prompt: str) -> str:
        """Internal method to handle input collection"""
        self.app.battle_log.write(prompt)
        self.input_event.clear()
        await self.input_event.wait()
        return pattern.sub('', self.input_value).upper()

    def on_input_submitted(self, event: Input.Submitted):
        """Handle when user submits input"""
        self.app.battle_log.write(f"> {pattern.sub('', event.value).upper()}")
        self.input_value = event.value
        self.input_event.set()
        event.input.clear()

    async def main_flow(self):
        """Override this in subclasses to define screen logic"""
        raise NotImplementedError("Subclasses must implement main_flow.")

"""Screens."""
class FortifyScreen(GameScreen):

    async def main_flow(self):
        # Import here to avoid circular dependencies
        from game.sample_logic import fortify_logic
        await fortify_logic(self.io)

class SojournScreen(GameScreen):

    async def main_flow(self):
        # Import here to avoid circular dependencies
        from game.sample_logic import sojourn_logic
        await sojourn_logic(self.io)

class BattleScreen(GameScreen):

    async def main_flow(self):
        # Import here to avoid circular dependencies
        from game.sample_logic import battle_logic
        await battle_logic(self.io)

class Game(App):

    SCREENS = { "fortify": FortifyScreen, "sojourn": SojournScreen, "battle": BattleScreen }

    def __init__(self):
        super().__init__()
        self.battle_log = BattleLog(id="battle-log", wrap=True, markup=True)

    def on_mount(self):
        self.push_screen("fortify")
