import sys

sys.path.insert(0, "../")

from api_chat.chatevents import ChatEvent


def make_events_json(*events):
    EVENT_ENUM_TO_STRINGS = {
        ChatEvent.CHAT_READY: "connected",
        ChatEvent.CHAT_WAITING: "waiting",
        ChatEvent.CHAT_ENDED: "strangerDisconnected",
        ChatEvent.GOT_MESSAGE: "gotMessage",
        ChatEvent.PARTNER_STARTED_TYPING: "typing",
        ChatEvent.PARTNER_STOPPED_TYPING: "stoppedTyping",
        ChatEvent.GOT_SERVER_NOTICE: "serverMessage",
        ChatEvent.CHAT_QUESTION: "dummy:question",
        ChatEvent.CHAT_COMMONLIKES: "dummy:common_likes",
    }

    events_json = [
        (EVENT_ENUM_TO_STRINGS[event], argument) for event, argument in events
    ]
    return events_json
