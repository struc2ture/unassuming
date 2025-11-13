from entity import Entity, Actor, Stats

PLAYER = Actor.actor_template(
    glyph="@",
    color=(255, 255, 255),
    name="Player",
    description="Player Description",
    stats=Stats(10, 10, 2, 1)
)

CRANE = Actor.actor_template(
    glyph="c",
    color=(160, 30, 140),
    name="Crane",
    description="Crane Description",
    stats=Stats(3, 3, 1, 1)
)

BULB = Actor.actor_template(
    glyph="B",
    color=(30, 100, 30),
    name="Bulb",
    description="Bulb Description",
    stats=Stats(15, 15, 3, 3)
)
