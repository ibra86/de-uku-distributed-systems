import asyncio
from pathlib import Path
from random import uniform


def get_file_name(fpath):
    return Path(fpath).stem


async def sleep_ms(min_sleep=0, max_sleep=1000):
    s = round(uniform(min_sleep, max_sleep))
    await asyncio.sleep(s / 1000)
    return s
