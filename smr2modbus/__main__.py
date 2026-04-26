from __future__ import annotations

import argparse
import asyncio
import logging

from .config import load_config
from .health import run_health_server
from .ingest import run_telnet_ingest
from .modbus_server import run_modbus_server
from .state import BridgeState


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SMR v5 to Modbus bridge")
    parser.add_argument("--config", required=True, help="Path to TOML config")
    parser.add_argument("--health-port", type=int, default=8080, help="HTTP health server port")
    return parser.parse_args()


async def _run() -> None:
    args = parse_args()
    config = load_config(args.config)
    state = BridgeState()

    await asyncio.gather(
        run_telnet_ingest(config, state),
        run_modbus_server(config.modbus, state),
        run_health_server(config.health, state, port=args.health_port),
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(_run())


if __name__ == "__main__":
    main()
