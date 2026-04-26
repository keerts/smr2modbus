from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class InputConfig:
    host: str
    port: int
    connect_timeout_s: float
    max_backoff_s: float


@dataclass(frozen=True)
class ModbusConfig:
    host: str
    port: int
    unit_id: int
    word_order: str
    log_register_queries: bool


@dataclass(frozen=True)
class PointConfig:
    name: str
    address: int
    data_type: str
    scale: float


@dataclass(frozen=True)
class HealthConfig:
    freshness_threshold_s: float


@dataclass(frozen=True)
class AppConfig:
    input: InputConfig
    modbus: ModbusConfig
    health: HealthConfig
    points: dict[str, PointConfig]


def _require(table: dict, key: str):
    if key not in table:
        raise ValueError(f"Missing required config key: {key}")
    return table[key]


def load_config(path: str | Path) -> AppConfig:
    with open(path, "rb") as f:
        raw = tomllib.load(f)

    input_table = _require(raw, "input")
    modbus_table = _require(raw, "modbus")
    health_table = _require(raw, "health")
    points_table = _require(raw, "points")

    word_order = _require(modbus_table, "word_order")
    if word_order not in {"high_to_low", "low_to_high"}:
        raise ValueError("modbus.word_order must be 'high_to_low' or 'low_to_high'")

    points: dict[str, PointConfig] = {}
    for name, cfg in points_table.items():
        points[name] = PointConfig(
            name=name,
            address=int(_require(cfg, "address")),
            data_type=str(_require(cfg, "data_type")),
            scale=float(_require(cfg, "scale")),
        )

    return AppConfig(
        input=InputConfig(
            host=str(_require(input_table, "host")),
            port=int(_require(input_table, "port")),
            connect_timeout_s=float(input_table.get("connect_timeout_s", 5.0)),
            max_backoff_s=float(input_table.get("max_backoff_s", 30.0)),
        ),
        modbus=ModbusConfig(
            host=str(_require(modbus_table, "host")),
            port=int(_require(modbus_table, "port")),
            unit_id=int(_require(modbus_table, "unit_id")),
            word_order=word_order,
            log_register_queries=bool(modbus_table.get("log_register_queries", False)),
        ),
        health=HealthConfig(
            freshness_threshold_s=float(health_table.get("freshness_threshold_s", 10.0))
        ),
        points=points,
    )
