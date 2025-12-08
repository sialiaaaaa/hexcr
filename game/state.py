import game.events as events
from enum import Enum, auto
import humanize, inflect

inflector = inflect.engine()

class Flag(Enum):
    SEEN_CHARACTER_CREATION = auto()
    SEEN_FORTIFY_INTRO = auto()

class Player:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.level = self._calculate_level(self.attributes)
        self.max_hp = self._calculate_max_hp(self.attributes, self.level)
        self.hp = self.max_hp
        self.position = None
        self.inventory = []

    def _calculate_level(self, attributes):
        return sum(attributes.values())

    def _calculate_max_hp(self, attributes, level):
        return (20-attributes["frailty"])*level

    def index(self):
        return humanize.natural_list(self.inventory) if self.inventory else "nothing"

    def recapitulate(self):
        return f"""Your name is [red]{self.name}[/red], burdened {inflector.number_to_words(self.level)} {"time" if self.level == 1 else "times"} over. You are possessed of:
    {inflector.number_to_words(self.attributes["frailty"]).capitalize()} [yellow]frailty[/yellow],
    {inflector.number_to_words(self.attributes["gracelessness"]).capitalize()} [yellow]gracelessness[/yellow],
    {inflector.number_to_words(self.attributes["caprice"]).capitalize()} [yellow]caprice[/yellow],
    {inflector.number_to_words(self.attributes["misfortune"]).capitalize()} [yellow]misfortune[/yellow],
    and {inflector.number_to_words(self.hp)} [yellow]credulity[/yellow], out of a possible {inflector.number_to_words(self.max_hp)}.
"""

class GameState:
    def __init__(self):
        self.player = None
        self.flags = set()
        self.screen = None

    def set_flag(self, flag: Flag):
        self.flags.add(flag)
    def check_flag(self, flag: Flag):
        return flag in self.flags
    def clear_flag(self, flag: Flag):
        self.flags.discard(flag)
