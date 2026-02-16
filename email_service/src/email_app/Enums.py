from enum import IntEnum


class EventType(IntEnum):
    CREATED = 1
    SENT = 2
    REJECTED = 3
    ATTENDANCE_CONFIRMED = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]