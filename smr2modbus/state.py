from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import threading

from .registers import RegisterSnapshot


@dataclass
class BridgeStatus:
    connected: bool = False
    last_error: str | None = None
    last_valid_update: datetime | None = None


class BridgeState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._registers: dict[int, int] = {}
        self._status = BridgeStatus()

    def set_connected(self, connected: bool) -> None:
        with self._lock:
            self._status.connected = connected

    def set_error(self, message: str) -> None:
        with self._lock:
            self._status.last_error = message

    def update_snapshot(self, snapshot: RegisterSnapshot) -> None:
        now = datetime.now(tz=timezone.utc)
        with self._lock:
            self._registers = snapshot.registers
            self._status.last_valid_update = now
            self._status.last_error = None

    def read_register(self, address: int) -> int:
        with self._lock:
            return self._registers.get(address, 0)

    def status(self) -> BridgeStatus:
        with self._lock:
            return BridgeStatus(
                connected=self._status.connected,
                last_error=self._status.last_error,
                last_valid_update=self._status.last_valid_update,
            )
