from dataclasses import dataclass, field
from typing import Set, Dict, Any, List
import random, json

@dataclass
class Adjective:
    word: str
    tags: Set[str]
    effects: Dict[str, Any] = field(default_factory=dict)

    def can_modify(self, noun):
        return bool(self.tags & noun.tags)

@dataclass
class Noun:
    word: str
    tags: Set[str]
    effects: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NounPhrase:
    adjective: Adjective
    noun: Noun

    @property
    def name(self):
        return f"{self.adjective.word} {self.noun.word}"


    @property
    def effects(self):
        result = {}
        adj_effects = self.adjective.effects
        noun_effects = self.noun.effects

        all_keys = set(adj_effects.keys()) | set(noun_effects.keys())

        for key in all_keys:
            adj_val = adj_effects.get(key)
            noun_val = noun_effects.get(key)

            # Key only in one dictionary
            if adj_val is None:
                result[key] = noun_val
            elif noun_val is None:
                result[key] = adj_val
            # Key in both - same value (redundant)
            elif adj_val == noun_val:
                result[key] = adj_val
            # Key in both - both are integers
            elif isinstance(adj_val, int) and isinstance(noun_val, int):
                result[key] = adj_val + noun_val
            # Key in both - not both integers
            else:
                # Helper to flatten values into a list
                def to_list(val):
                    if isinstance(val, list):
                        return val
                    else:
                        return [val]

                result[key] = to_list(adj_val) + to_list(noun_val)

        return result



class Generator:
    def __init__(self):
        self.adjectives = []
        self.nouns = []

    def add_adjective(self, word, tags, effects):
        self.adjectives.append(Adjective(word, tags, effects or {}))

    def add_noun(self, word, tags, effects):
        self.nouns.append(Noun(word, tags, effects or {}))

    def load_from_json(self, filename: str):
        """Load adjectives and nouns from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)

        # Load adjectives
        for adj_data in data.get('adjectives', []):
            self.add_adjective(
                word=adj_data['word'],
                tags=set(adj_data.get('tags', [])),
                effects=adj_data.get('effects', {})
            )

        # Load nouns
        for noun_data in data.get('nouns', []):
            self.add_noun(
                word=noun_data['word'],
                tags=set(noun_data.get('tags', [])),
                effects=noun_data.get('effects', {})
            )

    def get_compatible_adjectives(self, noun):
        return [adj for adj in self.adjectives if adj.can_modify(noun)]

    def generate_random(self, required_tags=None):
        if required_tags:
            valid_nouns = [n for n in self.nouns if required_tags & n.tags]
        else:
            valid_nouns = self.nouns

        if not valid_nouns:
            raise ValueError("No valid nouns for tag")

        noun = random.choice(valid_nouns)
        valid_adjectives = self.get_compatible_adjectives(noun)

        if not valid_adjectives:
            raise ValueError("No valid adjectives for tag")

        adjective = random.choice(valid_adjectives)

        return NounPhrase(adjective, noun)
