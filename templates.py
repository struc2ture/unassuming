from typing import List
import textwrap

from dialog import CharacterLine, PlayerLine
from dice import Dice
from entity import Entity, Actor, Stats
from entity import Item, ItemEquippable, EquipSlot

PLAYER = Actor.actor_template(
    glyph="@",
    color=(255, 255, 255),
    name="Player",
    description=textwrap.dedent("""\
        The you that you call "I". And I, occasionally, call "you", at other times - "adventurer" (when I'm not in the mood).
        You descended into the caverns when you were tormented by your craving for Bodily Riches.
        Did you forget?
        And what is your name? Did you forget again? I'm weary of reminding you."""),
    stats=Stats(10, 10, Dice.from_expr("1d4"), 1)
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

FOES: List[Actor] = [CRANE, BULB]

class USHER_DIALOG:
    C: List[CharacterLine] = [CharacterLine() for _ in range(50)]
    P: List[PlayerLine] = [PlayerLine() for _ in range(50)]

    C[0].init("Ah! A new visitor! My dearest of guests, I hope you enjoy your stay at this unassuming cavern that I happen to call my home.", [], C[1])
    C[1].init("There is someone for everyone here!", [], C[2])
    C[2].init("Looking for gold? You will find plenty of it here.", [], C[3])
    C[3].init("Looking for riches? I already mentioned the gold! But this dungeon is a place of business too! - A perfect investment opportunity!", [], C[4])
    C[4].init("Looking for fame? This is the place where LEGENDS are born. And MYTHS are disseminated. And now you are PART OF IT.", [], C[5])
    C[5].init("You've heard of the dangers this place entombs, but you are tough, you are a hero! Those stories are all written for someone else!", [], C[6])
    C[6].init("Don't bother turning around and looking for the exit... A completely natural and non-magical landslide oh so conveniently sealed the door behind you. I guess you will just have to stay and explore a little bit!", [], C[7])
    C[7].init("Not to worry! I am here to soften the blows and harden the steel!")

    start = C[0]

USHER = Actor.actor_template(
    glyph="U",
    color=(50, 80, 50),
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

A_MEEK_MAN = Actor.actor_template(
    glyph="⌡",
    color=(0, 0, 0),
    name="A Meek Man",
    description=textwrap.dedent("""\
        <Description>"""),
    stats=Stats(),
    is_hostile=False,
    dialog=CharacterLine().init("Hi.")
)

A_LORD = Actor.actor_template(
    glyph="Ç",
    color=(0, 0, 0),
    name="A Lord",
    description=textwrap.dedent("""\
        <Description>"""),
    stats=Stats(),
    is_hostile=False,
    dialog=CharacterLine().init("Eat.")
)

ILLITERATE = Actor.actor_template(
    glyph="ö",
    color=(0, 0, 0),
    name="An Illiterate",
    description=textwrap.dedent("""\
        <Description>"""),
    stats=Stats(),
    is_hostile=False,
    dialog=CharacterLine().init("Hi.")
)

FOREIGN = Actor.actor_template(
    glyph="Σ",
    color=(0, 0, 0),
    name="A Foreign NPC",
    description=textwrap.dedent("""\
        <Description>"""),
    stats=Stats(),
    is_hostile=False,
    dialog=CharacterLine().init("Hi.")
)

A_DEPOSED_KIND = Actor.actor_template(
    glyph="Ü",
    color=(0, 0, 0),
    name="A Deposed King",
    description=textwrap.dedent("""\
        <Description>"""),
    stats=Stats(),
    is_hostile=False,
    dialog=CharacterLine().init("Hi.")
)

AN_ENVOY = Actor.actor_template(
    glyph="É",
    color=(0, 0, 0),
    name="An Envoy",
    description=textwrap.dedent("""\
        <Description>"""),
    stats=Stats(),
    is_hostile=False,
    dialog=CharacterLine().init("Hi.")
)

A_TRANSLATOR = Actor.actor_template(
    glyph="τ",
    color=(0, 0, 0),
    name="Envoy's Translator",
    description=textwrap.dedent("""\
        <Description>"""),
    stats=Stats(),
    is_hostile=False,
    dialog=CharacterLine().init("Hi.")
)


NPCS: List[Actor] = [A_MEEK_MAN, A_LORD, ILLITERATE, FOREIGN, A_DEPOSED_KIND, AN_ENVOY, A_TRANSLATOR]

DAGGER = Item.item_template(
    glyph="/",
    color=(0, 191, 255),
    name="Dagger",
    description=textwrap.dedent("""\
        A dull (and uninteresting) dagger you stole off a body in front of the entrance to the cavern.
        This will have to do, for the lack of better foresight.
        The dagger was buried deep in the eye of the unlucky victim.
        With the gruesome image still stuck in your head, your gut tells you the wound was self-inflicted."""),
    equippable=ItemEquippable(EquipSlot.WEAPON, modified_attack=Dice.from_expr("1d6"))
)

SWORD = Item.item_template(
    glyph="/",
    color=(200, 191, 255),
    name="Sword",
    description=textwrap.dedent("""\
        A shiny steel sword, covered with tiny scratches.
        Purest iron ore from the mines of Hgilut infused with ivory charcoal. Each sword is thought to have a soul of an elephant.
        The sword has seen its share of combat and could use some sharpening. But so what? You only have to swing a little harder."""),
    equippable=ItemEquippable(EquipSlot.WEAPON, modified_attack=Dice.from_expr("1d8"))
)

A_TRINKET = Item.item_template(
    glyph="♦︎",
    color=(100, 100, 255),
    name="A Trinket",
    description=textwrap.dedent("""\
        A little trinket to add some bulk to your pouch.
        As the saying goes, 'False prophets wear empty pockets.'
        """),
)
