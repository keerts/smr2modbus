from __future__ import annotations

import asyncio
import logging

from .config import AppConfig
from .framer import TelegramFramer
from .parser import ParseError, parse_metrics
from .registers import build_register_snapshot
from .state import BridgeState


async def run_telnet_ingest(config: AppConfig, state: BridgeState) -> None:
    backoff = 1.0

    while True:
        state.set_connected(False)
        writer = None
        try:
            logging.info("Connecting to telnet stream %s:%s", config.input.host, config.input.port)
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(config.input.host, config.input.port),
                timeout=config.input.connect_timeout_s,
            )
            state.set_connected(True)
            backoff = 1.0
            framer = TelegramFramer()
            logging.info("Connected to telegram source")

            while True:
                chunk = await reader.read(4096)
                if not chunk:
                    raise ConnectionError("Source closed connection")

                frames = framer.feed(chunk.decode("ascii", errors="ignore"))
                for frame in frames:
                    try:
                        metrics = parse_metrics(frame)
                        snapshot = build_register_snapshot(config, metrics)
                        state.update_snapshot(snapshot)
                    except ParseError as exc:
                        state.set_error(str(exc))
                        logging.warning("Telegram parse failed: %s", exc)

        except Exception as exc:
            state.set_error(str(exc))
            state.set_connected(False)
            logging.warning("Ingest disconnected: %s", exc)
            logging.info("Reconnect in %.1f seconds", backoff)
            await asyncio.sleep(backoff)
            backoff = min(config.input.max_backoff_s, backoff * 2)
        finally:
            if writer is not None:
                writer.close()
                await writer.wait_closed()
