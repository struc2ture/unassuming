import textwrap

from dice import Dice
from entity import Entity, Actor, Stats

PLAYER = Actor.actor_template(
    glyph="@",
    color=(255, 255, 255),
    name="Player",
    description=textwrap.dedent("""\
        The you that you call "I". And I, occasionally, call "you", at other times - "adventurer" (when I'm not in the mood).
        You descended into the caverns when you were tormented by your craving for Bodily Riches.
        Did you forget?
        And what is your name? Did you forget again? I'm weary of reminding you."""),
    stats=Stats(10, 10, Dice.from_expr("1d6"), 1)
)

CRANE = Actor.actor_template(
    glyph="c",
    color=(160, 30, 140),
    name="Crane",
    description=textwrap.dedent("""\
        A long-necked manifestation. Whoever called it a "bird" could not have played a crueler joke.
        It is a vestigial structure of a long-forgotten chimera that used crane-like-arms to reach into deep and narrow cavities.
        Swarms of cranes have been harassing adventurers for centuries.
        While relatively harmless individually - nothing more than swatting a fly, leaving a bloody splat, - extremely dangerous in groups."""),
    stats=Stats(3, 3, Dice.from_expr("1d3"), 0)
)

BULB = Actor.actor_template(
    glyph="B",
    color=(30, 100, 30),
    name="Bulb",
    description=textwrap.dedent("""\
        Bulb A bulbous shape. A mass of flesh. A mess of flashing, blinking eyes.
        It sees all, contemplates all. It acts little, conserving energy.
        Don't be so foolish to stand still: if you get hit by the bulb,  you will not just feel embarrassed by your lack of agility - you will also most certainly feel the life drain out of your behind."""),
    stats=Stats(15, 15, Dice.from_expr("2d6"), 3)
)
