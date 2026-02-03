from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class TempFile:
    path: Path

    def cleanup(self) -> None:
        try:
            os.remove(self.path)
        except FileNotFoundError:
            return


def create_temp_file(suffix: str) -> TempFile:
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return TempFile(path=Path(path))


def cleanup_files(files: Iterable[TempFile]) -> None:
    for temp_file in files:
        temp_file.cleanup()
