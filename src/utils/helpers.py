import asyncio
from pathlib import Path
from random import uniform

from model import MessageCounter


def get_file_name(fpath):
    return Path(fpath).stem


async def sleep_ms(min_sleep=0, max_sleep=1000):
    s = round(uniform(min_sleep, max_sleep))
    await asyncio.sleep(s / 1000)
    return s


def cleanup(messages: list[MessageCounter]):
    sorted_messages = sorted(messages, key=lambda x: x.counter)
    unique_messages = []
    for m in sorted_messages:
        if m.counter not in set(u.counter for u in unique_messages):
            unique_messages.append(m)
    return unique_messages
