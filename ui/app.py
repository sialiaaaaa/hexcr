from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import RichLog, Input

from asyncio import Event

import re
pattern = re.compile('[\W_]+')

import game.sample_logic as sample_logic

"""Various widgets for use across various screens."""
class InputField(Input):
    DEFAULT_CSS = "InputField { dock: bottom; border: aliceblue; }"

class BattleLog(RichLog):
    can_focus = False
    DEFAULT_CSS = "BattleLog { height: 1fr; border: aliceblue; }"

"""Screens."""
class FortifyScreen(Screen):
    def __init__(self):
        super().__init__()
        self.input_value = None
        self.input_event = Event()

    def compose(self):
        yield BattleLog(id="output", wrap=True, markup=True)
        yield InputField(id="input", placeholder="Supply input...")

    def on_mount(self):
        self.run_worker(self.main_flow())

    def print(self, message):
        log = self.screen.query_one("#output", RichLog)
        log.write(message)

    async def get_input(self, prompt: str) -> str:
        self.print(prompt)
        self.input_event.clear()
        await self.input_event.wait()
        return pattern.sub('', self.input_value).upper()

    def on_input_submitted(self, event: InputField.Submitted):
        self.print(f"> {event.value.upper()}")
        self.input_value = event.value
        self.input_event.set()
        event.input.clear()

    async def main_flow(self):
        sample_logic.write_some_prompts(self)

class SojournScreen(Screen):
    def compose(self):
        yield Placeholder(id="sojourn")

class BattleScreen(Screen):
    def compose(self):
        yield Placeholder(id="battle")

class Game(App):

    SCREENS = { "fortify_screen": FortifyScreen, "sojourn_screen": SojournScreen, "battle_screen": BattleScreen }

    def on_mount(self):
        self.push_screen("fortify_screen")
