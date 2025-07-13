from pathlib import Path


def load_static() -> Path:
    """
        Load the path to the static files directory.

        This function constructs the path to the 'static' directory located
        three levels up from the current file's directory and resolves it to
        an absolute path. If the directory does not exist, it raises a
        FileNotFoundError.

        Returns:
            Path: An absolute Path object pointing to the 'static' directory.

        Raises:
            FileNotFoundError: If the 'static' directory does not exist.
    """
    return (Path(__file__).parent.parent.parent / 'static').resolve(strict=True)
