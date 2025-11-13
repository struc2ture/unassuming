from dataclasses import dataclass
import random
import re

@dataclass
class Dice:
    count: int = 1
    sides: int = 1
    bonus: int = 0

    @classmethod
    def from_expr(cls, expr: str):
        match = re.fullmatch(r"(\d*)d(\d+)([+-]\d+)?", expr.replace(" ", ""))
        if not match:
            raise ValueError(f"Invalid dice expression: {expr}")

        count = int(match.group(1) or 1)
        sides = int(match.group(2))
        bonus = int(match.group(3) or 0)
        return cls(count, sides, bonus)

    def roll(self) -> int:
        total = sum(random.randint(1, self.sides) for _ in range(self.count))
        return total + self.bonus

    def __str__(self) -> str:
        return f"{self.count}d{self.sides}+{self.bonus}"
