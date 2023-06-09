import json

from _abstractchat import _AbstractChat
from _common import requests, _START_SPY_URL, _validate_status_code  # patched
from chatevents import ChatEvent
from exceptions import apichatException


class Threesome(_AbstractChat):
    """Represents a chat with a partner with common interests."""

    def __init__(self, language="en"):
        """Constructor.
        Arguments:
            - language = "en" (str): The language in which to converse.
              This must be a language code defined in ISO 639-1. The
              languages Cebuano (ceb) and Filipino (fil) are also
              supported, but only defined in ISO 639-2. Some languages
              supported on the Omegle website are not supported because
              they are ambiguous.
        Return:
            - No return value.
        """
        super().__init__(language=language)

    def start(self):
        """Start looking for a partner.
        Ask the server to start looking for a question and also the partner to discuss the question with . Ideally, the server returns a client ID. If the
        client ID is obtained successfully, add initial events to the
        event queue and return.
        Raise:
            - PythonOmegleException if the response's status code is not
              200.
            - PythonOmegleException if the response does not include a
              client ID.
        Return:
            - No return value.
        """
        response = requests.get(
            self._server_url
            + _START_SPY_URL.format(
                self._random_id,  # randid
                self.language,  # lang
            )
        )

        _validate_status_code(response=response)
        json_data = json.loads(response.text)

        try:
            self._chat_id = json_data["clientID"]
        except KeyError:
            raise apichatException("Failed to get chat ID.")

        try:
            events_json = json_data["events"]
        except KeyError:
            return
        self._classify_events_and_add_to_queue(events_json=events_json)

    def _classify_events_and_add_to_queue(self, events_json):
        """Classify the events and push them to the event queue.
        event[0]=>event type
        event[0][0]=>"common likes"
        event[0][1]=>"common interests"

        """
        for event in events_json:
            event_type = event[0]

            if event_type == "connected":
                self._chat_ready_flag = True
                for event_ in events_json:
                    if event_[0] == "question":
                        question = event_[1]
                self._events.put((ChatEvent.CHAT_READY, question))

            elif event_type == "waiting":
                self._events.put((ChatEvent.CHAT_WAITING, None))

            elif event_type == "typing":
                if not self._chat_ready_flag:
                    # Simulate a 'chat ready' event
                    self._events.put((ChatEvent.CHAT_READY, None))
                    self._chat_ready_flag = True
                self._events.put((ChatEvent.PARTNER_STARTED_TYPING, None))

            elif event_type == "stoppedTyping":
                # TODO Check flag here too?
                self._events.put((ChatEvent.PARTNER_STOPPED_TYPING, None))

            elif event_type == "gotMessage":
                if not self._chat_ready_flag:
                    # Simulate a 'chat ready' event
                    self._events.put((ChatEvent.CHAT_READY, None))
                    self._chat_ready_flag = True
                message = event[1]
                self._events.put((ChatEvent.GOT_MESSAGE, message))

            elif event_type == "strangerDisconnected":
                if not self._chat_ready_flag:
                    # Simulate a 'chat ready' event
                    self._events.put((ChatEvent.CHAT_READY, None))
                self._events.put((ChatEvent.CHAT_ENDED, None))
                self._chat_ready_flag = False

            elif event_type == "serverMessage":
                # TODO Check flag here too?
                notice = event[1]
                self._events.put((ChatEvent.GOT_SERVER_NOTICE, notice))

            elif event_type == "identDigests":
                # Included after a partner was found, may be ignored.
                pass

            elif event_type == "recaptchaRequired":
                raise apichatException("ReCAPTCHA check required.")
