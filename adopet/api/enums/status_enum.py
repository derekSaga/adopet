from enum import Enum


class StatusEnum(Enum):
    NEW = 'NEW'
    AVAILABLE = 'AVAILABLE'
    ADOPET = 'ADOPET'
    QUARANTINE = 'QUARANTINE'
    REMOVED = 'REMOVED'
    SUSPENDED = 'SUSPENDED'
