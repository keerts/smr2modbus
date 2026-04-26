from __future__ import annotations

from dataclasses import dataclass

from .config import AppConfig
from .parser import ParsedMetrics


def _clamp_u32(value: int) -> int:
    return max(0, min(0xFFFFFFFF, value))


def _clamp_i32(value: int) -> int:
    return max(-0x80000000, min(0x7FFFFFFF, value))


def _to_raw(value: float, scale: float) -> int:
    return int(round(value / scale))


def split_u32_words(raw: int, word_order: str) -> tuple[int, int]:
    raw = _clamp_u32(raw)
    hi = (raw >> 16) & 0xFFFF
    lo = raw & 0xFFFF
    if word_order == "high_to_low":
        return hi, lo
    return lo, hi


def split_i32_words(raw: int, word_order: str) -> tuple[int, int]:
    raw = _clamp_i32(raw)
    raw_u = raw & 0xFFFFFFFF
    hi = (raw_u >> 16) & 0xFFFF
    lo = raw_u & 0xFFFF
    if word_order == "high_to_low":
        return hi, lo
    return lo, hi


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
        if point.data_type == "uint32":
            first, second = split_u32_words(raw, config.modbus.word_order)
        elif point.data_type == "int32":
            first, second = split_i32_words(raw, config.modbus.word_order)
        else:
            raise ValueError(f"Unsupported point data type: {point.data_type}")

        out[point.address] = first
        out[point.address + 1] = second

    return RegisterSnapshot(registers=out)
