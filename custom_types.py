from typing import TypedDict


class EventType(TypedDict):
    hour: int
    minute: int
    type: str
    seconds: int
    message: bool
    rotation_minutes: int


class BossRotation(TypedDict):
    rotation: list[str]
    special_bosses: dict[str, str]
