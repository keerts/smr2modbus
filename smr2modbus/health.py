from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import json

from .config import HealthConfig
from .state import BridgeState


def _health_payload(config: HealthConfig, state: BridgeState) -> tuple[int, dict]:
    status = state.status()
    now = datetime.now(tz=timezone.utc)
    stale = True
    age_seconds = None
    if status.last_valid_update is not None:
        age_seconds = (now - status.last_valid_update).total_seconds()
        stale = age_seconds > config.freshness_threshold_s

    ready = status.connected and status.last_valid_update is not None and not stale
    code = 200 if ready else 503
    payload = {
        "ready": ready,
        "connected": status.connected,
        "stale": stale,
        "age_seconds": age_seconds,
        "last_error": status.last_error,
    }
    return code, payload


async def run_health_server(config: HealthConfig, state: BridgeState, host: str = "0.0.0.0", port: int = 8080) -> None:
    async def _handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            await reader.readuntil(b"\r\n\r\n")
        except Exception:
            writer.close()
            await writer.wait_closed()
            return

        status_code, payload = _health_payload(config, state)
        body = json.dumps(payload).encode("utf-8")
        reason = "OK" if status_code == 200 else "Service Unavailable"
        response = (
            f"HTTP/1.1 {status_code} {reason}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode("ascii") + body
        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(_handler, host=host, port=port)
    async with server:
        await server.serve_forever()
