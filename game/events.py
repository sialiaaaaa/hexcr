from game.state import Player
import inflect

inflector = inflect.engine()

class Event:
    def __init__(self, io):
        self.io = io
        self.state = io.state

    async def run(self):
        raise NotImplementedError

class CreateCharacter(Event):
    async def run(self):
        while True:
            name = await self.io.get_input("In parts beyond they have called you by many names. Here you will be known as...")
            if name:
                verify = await self.io.get_input(f"Your name is [red]{name}[/red]. Is this acceptable?")
                if verify in ["YES", "Y"]:
                    break
                else:
                    self.io.print("Then I ask again:")
            else:
                self.io.print("Why do you falter?")

        while True:
            points = 10
            statistic_dict = {"strength": 0, "dexterity": 0, "conviction": 0, "luck": 0}
            for i, statistic in enumerate(statistic_dict):
                while True:
                    if i == 0:
                        allotment = await self.io.get_input(f"Your [yellow]attributes[/yellow] must now be determined. You have [blue]{inflector.number_to_words(points)} points[/blue] to distribute across four [yellow]statistics[/yellow]. How many will contribute to your [yellow]{statistic}[/yellow]?")
                    else:
                        allotment = await self.io.get_input(f"[blue]{inflector.number_to_words(points).capitalize()} {"point[/blue] remains" if points == 1 else "points[/blue] remain"}. How many will contribute to your [yellow]{statistic}[/yellow]?")

                    try:
                        if int(allotment) <= points:
                            points -= int(allotment)
                            statistic_dict[statistic] = int(allotment)
                            break
                    except ValueError:
                        pass
                    self.io.print("Submit a number; one which is less than the number of [blue]points[/blue] you have remaining.")

            self.io.print(f"You have expressed the desire for [yellow]attributes[/yellow] based on the following distribution of [blue]points[/blue]:")
            for i, (statistic, score) in enumerate(statistic_dict.items()):
                self.io.print(f"[blue]{inflector.number_to_words(score).capitalize()} {"point[/blue]" if score == 1 else "points[/blue]"} towards your [yellow]{statistic}[/yellow].")
            if points > 0:
                self.io.print(f"Note that [blue]{inflector.number_to_words(points)} {"point[/blue] remains" if points == 1 else "points[/blue] remain"}.")
            verify = await self.io.get_input("Is this acceptable?")
            if verify in ["YES", "Y"]:
                break
            else:
                self.io.print("Then we will begin again.")

        attributes = {"frailty": 20-statistic_dict["strength"], "gracelessness": 20-statistic_dict["dexterity"], "caprice": 20-statistic_dict["conviction"], "misfortune": 20-statistic_dict["luck"]}
        return Player(name, attributes)


