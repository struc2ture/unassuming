from dataclasses import dataclass

from dice import Dice

class Ability:
    name: str = "<Ability name>"
    pass

@dataclass
class LightningAbility(Ability):
    name = "Lightning"
    power: Dice
