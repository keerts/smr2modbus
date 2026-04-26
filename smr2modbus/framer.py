from __future__ import annotations


class TelegramFramer:
    def __init__(self) -> None:
        self._partial = ""
        self._in_frame = False
        self._lines: list[str] = []

    def feed(self, chunk: str) -> list[str]:
        self._partial += chunk
        frames: list[str] = []

        while True:
            newline = self._partial.find("\n")
            if newline < 0:
                break
            line = self._partial[:newline].rstrip("\r")
            self._partial = self._partial[newline + 1 :]

            if line.startswith("/"):
                self._in_frame = True
                self._lines = [line]
                continue

            if not self._in_frame:
                continue

            self._lines.append(line)

            if line.startswith("!") and len(line) >= 5:
                frames.append("\n".join(self._lines))
                self._lines = []
                self._in_frame = False

        return frames
