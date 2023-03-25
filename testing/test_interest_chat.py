import queue
import unittest
import api_chat
import sys

sys.path.insert(0, "../")

from api_chat.interestschat import InterestsChat
from api_chat.chatevents import ChatEvent
from api_chat.exceptions import PythonOmegleException
from api_chat._common import _SERVER_POOL

from common_tests import make_events_json


class InterestsChatTest(unittest.TestCase):
    def test_constructor(self):

        interests_not_list = r"Interests must be a list."
        with self.assertRaisesRegex(TypeError, interests_not_list):
            # Interests not a list instance
            InterestsChat(None)

        interests_elements_not_str = r"All interests must be strings."
        with self.assertRaisesRegex(TypeError, interests_elements_not_str):
            # Interest is not a str instance
            InterestsChat([42])

        with self.assertRaises(ValueError):
            # Interests list is empty
            InterestsChat([])

        language_not_str = r"Language must be a string."
        with self.assertRaisesRegex(TypeError, language_not_str):
            # Language not a str instance
            InterestsChat(["foo"], None)

        with self.assertRaises(ValueError):
            # Not in ISO 639-1 or ISO 639-2
            InterestsChat(["foo"], "french")
