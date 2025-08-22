from typing import TypedDict


class EventType(TypedDict):
    hour: int
    minute: int
    type: str
    boss_list: list[str]
    seconds: int
    is_first: bool
    rotation_minutes: int
