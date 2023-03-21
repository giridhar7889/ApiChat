import enum

__all__ = ["ChatEvent"]


class ChatEvent(enum.Enum):

    CHAT_READY = 1
    CHAT_WAITING = 2
    CHAT_ENDED = 3
    GOT_SERVER_NOTICE = 4
    GOT_MESSAGE = 5
    PARTNER_STARTED_TYPING = 6
    PARTNER_STOPPED_TYPING = 7
