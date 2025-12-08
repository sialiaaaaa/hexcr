import inflect
from generator.names import Generator
from pathlib import Path

inflector = inflect.engine()
gen = Generator()
gen.load_from_json(Path("generator/words.json"))

