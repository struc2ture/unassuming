from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player_desc = """
The you that you call "I". And I, occasionally, call "you", at other times - "adventurer" (when I'm not in the mood).
You descended into the caverns when you were tormented by your craving for Bodily Riches.
Did you forget?
And what is your name? Did you forget again? I'm weary of reminding you.
"""
player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

crane_desc = """
A long-necked manifestation. Whoever called it a "bird" could not have played a crueler joke.
It is a vestigial structure of a long-forgotten chimera that used crane-like-arms to reach into deep and narrow cavities.
Swarms of cranes have been harassing adventurers for centuries.
While relatively harmless individually - nothing more than swatting a fly, leaving a bloody splat, - extremely dangerous in groups.
"""
crane = Actor(
    char="c",
    color=(63, 127, 63),
    name="Crane",
    description=crane_desc,
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

bulb_desc = """
A bulbous shape. A mass of flesh. A mess of flashing, blinking eyes.
It sees all, contemplates all. It acts little, conserving energy.
Don't be so foolish to stand still: if you get hit by the bulb,  you will not just feel embarrassed by your lack of agility - you will also most certainly feel the life drain out of your behind.
"""
bulb = Actor(
    char="B",
    color=(0, 127, 0),
    name="Bulb",
    description="Bulb",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)


confusion_scroll_desc = """
Scramble a sentient mind if you so dare!
A scroll with an ancient, but terrifyingly lucid script.
When did you learn this language? Why does it feel so familiar?
"""
confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion scroll",
    description=confusion_scroll_desc,
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll_desc = """
Ancient magic forms a fiery sphere in your palms. It does not burn but the intended target.
Casting is easy, but terrifying: any thought about yourself during the recital results in instant self-immolation.
"""
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    description=fireball_scroll_desc,
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

lightning_scroll_desc = """
Seize the spears of electricity from the firmament, like the spears of asparagus from the soil of your meemaw's garden.
Static shock will seize the opponent, ionize them, vaporize them; turn them into dust, possibly plasma.
"""
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    description=lightning_scroll_desc,
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

health_potion_desc = """
A potion of rejuvenation. Origins unknown.
Possibly fermented pomegranate juice, possibly infused with the dried and possibly ground honeycomb-cap of a True Morel.
"""
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    description=health_potion_desc,
    consumable=consumable.HealingConsumable(amount=4),
)

dagger_desc = """
A dull (and uninteresting) dagger you stole off a body in front of the entrance to the cavern.
This will have to do, for the lack of better foresight.
The dagger was buried deep in the eye of the unlucky victim.
With the gruesome image still stuck in your head, your gut tells you the wound was self-inflicted.
"""
dagger = Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    description=dagger_desc,
    equippable=equippable.Dagger()
)

sword_desc = """
A shiny steel sword, covered with tiny scratches.
Purest iron ore from the mines of Hgilut infused with ivory charcoal. Each sword is thought to have a soul of an elephant.
The sword has seen its share of combat and could use some sharpening. But so what? You only have to swing a little harder.
"""
sword = Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    description=sword_desc,
    equippable=equippable.Sword()
)

leather_armor_desc = """
A traditional Neeman-style leather armor: panels of boarhide, boiled in pig's blood and stitched to a tough canvas base, the kind of cloth used to keep grain from spilling.
Many can't tolerate the smell, but you came to enjoy it, although you would not admit it to a fellow traveler sharing a campfire.
"""
leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    description=leather_armor_desc,
    equippable=equippable.LeatherArmor(),
)

chain_mail_desc = """
Interlocking rings made of case-hardened steel; each ring closed with a tiny rivet, crafted by a famous smith from the Mother of Cities, Bactra.
The chain mail, while being of the highest craftsmanship, is nearly a thousand years old. Some rings are undone. Some show signs of rust.
It will do for now, but you dream that once you escape this hellish dungeon and make it to Bactra, you will commission one just like this, from the very same smith (the rumor is, he is still alive).
"""
chain_mail = Item(
    char="[",
    color=(139, 69, 19),
    name="Chain Mail",
    description=chain_mail_desc,
    equippable=equippable.ChainMail()
)
