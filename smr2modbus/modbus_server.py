from __future__ import annotations

import asyncio
import struct

from .config import ModbusConfig
from .state import BridgeState


def _exception(function_code: int, code: int) -> bytes:
    return bytes([function_code | 0x80, code])


def _build_read_response(function_code: int, start: int, quantity: int, state: BridgeState) -> bytes:
    if quantity < 1 or quantity > 125:
        return _exception(function_code, 0x03)

    payload = bytearray()
    for offset in range(quantity):
        value = state.read_register(start + offset)
        payload.extend(struct.pack(">H", value))

    return bytes([function_code, len(payload)]) + bytes(payload)


async def _handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    config: ModbusConfig,
    state: BridgeState,
) -> None:
    try:
        while True:
            header = await reader.readexactly(7)
            transaction_id, protocol_id, length, unit_id = struct.unpack(">HHHB", header)
            if protocol_id != 0 or length < 2:
                return
            pdu = await reader.readexactly(length - 1)
            function_code = pdu[0]

            if unit_id != config.unit_id:
                continue

            if function_code not in {3, 4}:
                body = _exception(function_code, 0x01)
            elif len(pdu) != 5:
                body = _exception(function_code, 0x03)
            else:
                start, quantity = struct.unpack(">HH", pdu[1:5])
                body = _build_read_response(function_code, start, quantity, state)

            mbap = struct.pack(">HHHB", transaction_id, 0, len(body) + 1, unit_id)
            writer.write(mbap + body)
            await writer.drain()
    except asyncio.IncompleteReadError:
        pass
    finally:
        writer.close()
        await writer.wait_closed()


async def run_modbus_server(config: ModbusConfig, state: BridgeState) -> None:
    server = await asyncio.start_server(
        lambda r, w: _handle_client(r, w, config, state),
        host=config.host,
        port=config.port,
    )
    async with server:
        await server.serve_forever()
