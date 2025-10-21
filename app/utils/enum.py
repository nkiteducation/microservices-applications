import enum

class Memory(enum.IntEnum):
    B = 1
    KB = 1024 * B
    MB = 1024 * KB
    GB = 1024 * MB

class ContactMethod(enum.StrEnum):
    EMAIL = "email"
    PHONE = "phone"
    TELEGRAM = "telegram"
