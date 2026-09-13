from datetime import datetime, timedelta, timezone
import unittest

from smr2modbus.modbus_server import _build_read_response
from smr2modbus.registers import RegisterSnapshot
from smr2modbus.state import BridgeState


class ModbusFreshnessTests(unittest.TestCase):
    def test_fresh_snapshot_is_served(self) -> None:
        state = BridgeState()
        state.update_snapshot(RegisterSnapshot(registers={1: 123}))

        response = _build_read_response(4, 1, 1, state, freshness_threshold_s=10)

        self.assertEqual(response, bytes.fromhex("0402007b"))

    def test_missing_snapshot_returns_device_failure(self) -> None:
        state = BridgeState()

        response = _build_read_response(4, 1, 1, state, freshness_threshold_s=10)

        self.assertEqual(response, bytes.fromhex("8404"))

    def test_stale_snapshot_returns_device_failure(self) -> None:
        state = BridgeState()
        state.update_snapshot(RegisterSnapshot(registers={1: 123}))
        with state._lock:
            state._status.last_valid_update = datetime.now(tz=timezone.utc) - timedelta(seconds=11)

        response = _build_read_response(3, 1, 1, state, freshness_threshold_s=10)

        self.assertEqual(response, bytes.fromhex("8304"))


if __name__ == "__main__":
    unittest.main()
