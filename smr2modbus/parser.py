from __future__ import annotations

from dataclasses import dataclass
import re


_VALUE_RE = re.compile(r"^([0-9]+(?:\.[0-9]+)?)")


@dataclass(frozen=True)
class ParsedMetrics:
    current_l1_a: float
    current_l2_a: float
    current_l3_a: float
    real_power_l1_kw: float
    real_power_l2_kw: float
    real_power_l3_kw: float


class ParseError(ValueError):
    pass


def _extract_value(telegram: str, obis: str) -> float:
    needle = f"{obis}("
    for line in telegram.splitlines():
        if not line.startswith(needle):
            continue
        inner = line[len(needle) :]
        end = inner.find(")")
        if end < 0:
            break
        token = inner[:end]
        number = token.split("*", 1)[0]
        match = _VALUE_RE.match(number)
        if match is None:
            break
        return float(match.group(1))
    raise ParseError(f"Missing or invalid OBIS value: {obis}")


def parse_metrics(telegram: str) -> ParsedMetrics:
    current_l1 = _extract_value(telegram, "1-0:31.7.0")
    current_l2 = _extract_value(telegram, "1-0:51.7.0")
    current_l3 = _extract_value(telegram, "1-0:71.7.0")

    p_import_l1 = _extract_value(telegram, "1-0:21.7.0")
    p_import_l2 = _extract_value(telegram, "1-0:41.7.0")
    p_import_l3 = _extract_value(telegram, "1-0:61.7.0")
    p_export_l1 = _extract_value(telegram, "1-0:22.7.0")
    p_export_l2 = _extract_value(telegram, "1-0:42.7.0")
    p_export_l3 = _extract_value(telegram, "1-0:62.7.0")

    return ParsedMetrics(
        current_l1_a=current_l1,
        current_l2_a=current_l2,
        current_l3_a=current_l3,
        real_power_l1_kw=p_import_l1 - p_export_l1,
        real_power_l2_kw=p_import_l2 - p_export_l2,
        real_power_l3_kw=p_import_l3 - p_export_l3,
    )
