from __future__ import annotations

from dataclasses import dataclass

from .config import AppConfig
from .parser import ParsedMetrics


def _clamp_u16(value: int) -> int:
    return max(0, min(0xFFFF, value))


def _clamp_i16(value: int) -> int:
    return max(-0x8000, min(0x7FFF, value))


def _to_raw(value: float, scale: float) -> int:
    return int(round(value / scale))


@dataclass
class RegisterSnapshot:
    registers: dict[int, int]


def build_register_snapshot(config: AppConfig, metrics: ParsedMetrics) -> RegisterSnapshot:
    values = {
        "current_l1": metrics.current_l1_a,
        "current_l2": metrics.current_l2_a,
        "current_l3": metrics.current_l3_a,
        "current_n": 0.0,
        "real_power_l1": metrics.real_power_l1_kw,
        "real_power_l2": metrics.real_power_l2_kw,
        "real_power_l3": metrics.real_power_l3_kw,
    }

    out: dict[int, int] = {}
    for name, point in config.points.items():
        value = values[name]
        raw = _to_raw(value, point.scale)
        if point.data_type == "uint16":
            encoded = _clamp_u16(raw)
        elif point.data_type == "int16":
            encoded = _clamp_i16(raw) & 0xFFFF
        else:
            raise ValueError(f"Unsupported point data type: {point.data_type}")
        out[point.address] = encoded

    return RegisterSnapshot(registers=out)
