from smr2modbus.config import load_config
from smr2modbus.parser import parse_metrics
from smr2modbus.registers import build_register_snapshot
import tempfile
import textwrap
import unittest


SAMPLE_TELEGRAM = """/KFM5KAIFA-METER
1-3:0.2.8(50)
1-0:31.7.0(016*A)
1-0:51.7.0(000*A)
1-0:71.7.0(016*A)
1-0:21.7.0(03.917*kW)
1-0:41.7.0(00.000*kW)
1-0:61.7.0(03.820*kW)
1-0:22.7.0(00.000*kW)
1-0:42.7.0(00.000*kW)
1-0:62.7.0(00.000*kW)
!A32F
"""


def _config_text() -> str:
    return textwrap.dedent(
        f"""
        [input]
        host = "127.0.0.1"
        port = 23

        [modbus]
        host = "0.0.0.0"
        port = 1502
        unit_id = 1
        word_order = "high_to_low"

        [health]
        freshness_threshold_s = 10

        [points.current_l1]
        address = 1
        data_type = "uint16"
        scale = 0.01

        [points.current_l2]
        address = 2
        data_type = "uint16"
        scale = 0.01

        [points.current_l3]
        address = 3
        data_type = "uint16"
        scale = 0.01

        [points.current_n]
        address = 4
        data_type = "uint16"
        scale = 0.01

        [points.real_power_l1]
        address = 5
        data_type = "int16"
        scale = 0.001

        [points.real_power_l2]
        address = 6
        data_type = "int16"
        scale = 0.001

        [points.real_power_l3]
        address = 7
        data_type = "int16"
        scale = 0.001
        """
    )


class ParserRegisterTests(unittest.TestCase):
    def _load(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".toml") as f:
            f.write(_config_text())
            f.flush()
            return load_config(f.name)

    def test_parser_outputs_expected_metrics(self) -> None:
        metrics = parse_metrics(SAMPLE_TELEGRAM)
        self.assertEqual(metrics.current_l1_a, 16.0)
        self.assertEqual(metrics.current_l2_a, 0.0)
        self.assertEqual(metrics.current_l3_a, 16.0)
        self.assertEqual(metrics.real_power_l1_kw, 3.917)
        self.assertEqual(metrics.real_power_l2_kw, 0.0)
        self.assertEqual(metrics.real_power_l3_kw, 3.82)

    def test_register_encoding_compact_16bit(self) -> None:
        cfg = self._load()
        metrics = parse_metrics(SAMPLE_TELEGRAM)
        snapshot = build_register_snapshot(cfg, metrics)

        self.assertEqual(snapshot.registers[1], 1600)
        self.assertEqual(snapshot.registers[2], 0)
        self.assertEqual(snapshot.registers[3], 1600)
        self.assertEqual(snapshot.registers[4], 0)
        self.assertEqual(snapshot.registers[5], 3917)
        self.assertEqual(snapshot.registers[6], 0)
        self.assertEqual(snapshot.registers[7], 3820)
        self.assertNotIn(8, snapshot.registers)

    def test_register_clamp_compact_16bit(self) -> None:
        cfg = self._load()
        metrics = parse_metrics(
            """/KFM5KAIFA-METER
1-0:31.7.0(999*A)
1-0:51.7.0(000*A)
1-0:71.7.0(016*A)
1-0:21.7.0(99.999*kW)
1-0:41.7.0(00.000*kW)
1-0:61.7.0(00.000*kW)
1-0:22.7.0(00.000*kW)
1-0:42.7.0(00.000*kW)
1-0:62.7.0(99.999*kW)
!0000
"""
        )
        snapshot = build_register_snapshot(cfg, metrics)

        self.assertEqual(snapshot.registers[1], 65535)
        self.assertEqual(snapshot.registers[5], 32767)
        self.assertEqual(snapshot.registers[7], 0x8000)


if __name__ == "__main__":
    unittest.main()
