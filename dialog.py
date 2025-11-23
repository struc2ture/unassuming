from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class CharacterLine:
    text: str = "<...>"
    responses: List[PlayerLine] = field(default_factory=list)
    next_line: Optional[CharacterLine] = None
    action: Optional[str] = None

    def init(self, text: str, responses: Optional[List[PlayerLine]] = None, next_line: Optional[CharacterLine] = None, action: Optional[str] = None) -> CharacterLine:
        self.text = text
        self.responses = responses or []
        self.next_line = next_line
        self.action = action
        return self


@dataclass
class PlayerLine:
    text: str = "<...>"
    character_line: Optional[CharacterLine] = None

    def init(self, text: str, character_line: Optional[CharacterLine] = None) -> PlayerLine:
        self.text = text
        self.character_line = character_line
        return self


C: List[CharacterLine] = [CharacterLine() for _ in range(50)]
P: List[PlayerLine] = [PlayerLine() for _ in range(50)]

C[0].init("Hi.", [], C[1])
C[1].init("How can I help you?", [P[0], P[1], P[2], P[3]])

P[0].init("Tell me about yourself.", C[2])
P[1].init("I want to trade with YOU!", C[3])
P[2].init("You're a crazy old man!!!", C[4])
P[3].init("My only intention is to part ways.", None)

C[2].init("I am myself and I will leave it at that! Does that answer satisfy you?", [P[4]])

P[4].init("...I guess.", C[1])

C[3].init("...I guess. Let our junk switch its pockets' owners... If that's what pleases you.", [], C[1], "trade")
C[4].init("I may be crazy, but you are DEAD!!!", [], None, "turn_hostile")
