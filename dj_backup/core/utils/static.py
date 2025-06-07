from pathlib import Path


def load_static():
    return (Path(__file__).parent.parent.parent / 'static').resolve(strict=True)
