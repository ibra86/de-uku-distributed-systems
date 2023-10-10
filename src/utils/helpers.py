from pathlib import Path


def get_file_name(fpath):
    return Path(fpath).stem
