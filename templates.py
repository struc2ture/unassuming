from typing import List
import textwrap

from dialog import CharacterLine, PlayerLine
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
        It is a vestigial structure of a long-forgotten chimera that used its numerous crane-like-arms to reach into deep and narrow cavities.
        Swarms of cranes have been harassing adventurers for centuries.
        While relatively harmless individually - nothing more than swatting a fly, leaving a bloody splat, - extremely dangerous in groups."""),
    stats=Stats(3, 3, Dice.from_expr("1d3"), 0)
)

BULB = Actor.actor_template(
    glyph="B",
    color=(30, 100, 30),
    name="Bulb",
    description=textwrap.dedent("""\
        A bulbous shape. A mass of flesh. A mess of flashing, blinking eyes.
        It sees all, contemplates all. It acts little, conserving energy.
        Don't be so foolish to stand still: if you get hit by the bulb,  you will not just feel embarrassed by your lack of agility - you will also most certainly feel the life drain out from your behind."""),
    stats=Stats(15, 15, Dice.from_expr("2d6"), 3)
)

class USHER_DIALOG:
    C: List[CharacterLine] = [CharacterLine() for _ in range(50)]
    P: List[PlayerLine] = [PlayerLine() for _ in range(50)]

    C[0].init("Dearest of friends!!! Welcome to the dungeon!", [], C[1])
    C[1].init("Now, before you proceed, I must give you one single piece of advice!", [P[0]])

    P[0].init("...", C[2])

    C[2].init("Turn back. If it's not too late, if you still remember how you came in here, turn back and leave this godforsaken place.", [P[1]])

    P[1].init("...", C[3])

    C[3].init("Turn back I tell you!!!", [], C[4])
    C[4].init("You came here looking for glory and recognition... You're convinced the rumors about this place are for everyone else but you. And you may be right. Ohhhh you may be TOO right for your own damn good...", [], C[5])
    C[5].init("You will find all of it here. This place is dangerous, but you are a hero. It is true. I can see it in your eyes.", [], C[6])
    C[6].init("Nothing can hold you back. Nothing can stop you...", [P[2]])

    P[2].init("<Leave the man to continue his blabberings....>")

    start = C[0]

USHER = Actor.actor_template(
    glyph="U",
    color=(130, 200, 130),
    name="Usher",
    description=textwrap.dedent("""\
        This man looks suspiciously friendly for the kind of place you both find yourself in.
        As soon as he notices you, he makes eye contact and puts on a polite smile.
        You can smell an air of officiality in the vicinity. "Sandalwood and lilac," crosses your absent mind.
        The shine of the precious stone - diamond? - on the man's neck fills you with respect for the man, and a craving to apropriate the said respect for yourself."""),
    stats=Stats(20, 20, Dice.from_expr("2d10"), 3),
    is_hostile=False,
    dialog=USHER_DIALOG.start
)
