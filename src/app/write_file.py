from pathlib import Path


def write_file(filepath: str, string: str) -> None:
    with Path(filepath).open(mode="w") as file:
        file.write(string)
