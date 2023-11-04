from model import MessageCounter
from utils.helpers import cleanup


def test_cleanup():
    messages = [
        MessageCounter(name='msg_3', write_concern=2, counter=0),
        MessageCounter(name='msg_3', write_concern=2, counter=1),
        MessageCounter(name='msg_4', write_concern=3, counter=1),
        MessageCounter(name='msg_5', write_concern=1, counter=0),
        MessageCounter(name='msg_6', write_concern=4, counter=2),
    ]

    clean_messages = cleanup(messages)

    expected_messages = [
        MessageCounter(name='msg_3', write_concern=2, counter=0),
        MessageCounter(name='msg_3', write_concern=2, counter=1),
        MessageCounter(name='msg_6', write_concern=4, counter=2)
    ]

    assert clean_messages == expected_messages
