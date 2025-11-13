from dataclasses import dataclass, field
from typing import List

@dataclass
class TraceEntry:
    kind: str = "<Unknown kind>"
    items: List[str] = field(default_factory=list)

    def add_item(self, item: str) -> None:
        self.items.append(item)

    def __str__(self) -> str:
        item_sep = "\n  "
        item_str = f"\n  {item_sep.join(self.items)}" if len(self.items) > 0 else ""
        return f'{self.kind}{item_str}'


@dataclass
class GameTraceLog:
    entries: List[TraceEntry] = field(default_factory=list)

    def add_entry(self, kind: str) -> TraceEntry:
        new_entry = TraceEntry(kind)
        self.entries.append(new_entry)
        return new_entry

    def print_last(self, n: int = 1):
        print("\n---\n".join(str(entry) for entry in self.entries[-n:]))

    def get_str(self) -> str:
        return "\n---\n".join(str(entry) for entry in self.entries)

class GameTrace:
    log = GameTraceLog()

    @staticmethod
    def add_game_start():
        log_entry = GameTrace.log.add_entry("GAME_START")
        log_entry.add_item("message_from_world: hi!!!")
        log_entry.add_item("message_from_world: how are you!!!")

    @staticmethod
    def add_tick(turn: int):
        log_entry = GameTrace.log.add_entry("TICK")
        log_entry.add_item(f"turn: {turn}")
