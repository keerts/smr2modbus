from __future__ import annotations

import asyncio
import logging
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
    peer = writer.get_extra_info("peername")
    client = f"{peer[0]}:{peer[1]}" if isinstance(peer, tuple) and len(peer) >= 2 else "unknown"
    logging.info("Modbus client connected: %s", client)
    try:
        while True:
            header = await reader.readexactly(7)
            transaction_id, protocol_id, length, unit_id = struct.unpack(">HHHB", header)
            if config.log_protocol_debug:
                logging.info(
                    "Modbus MBAP from %s: raw=%s tx_id=%s proto=%s len=%s unit=%s",
                    client,
                    header.hex(),
                    transaction_id,
                    protocol_id,
                    length,
                    unit_id,
                )
            if protocol_id != 0 or length < 2:
                if config.log_register_queries:
                    logging.info(
                        "Modbus query ignored from %s: invalid_mbap protocol_id=%s length=%s",
                        client,
                        protocol_id,
                        length,
                    )
                return
            pdu = await reader.readexactly(length - 1)
            function_code = pdu[0]
            if config.log_protocol_debug:
                logging.info("Modbus PDU from %s: raw=%s", client, pdu.hex())

            if unit_id != config.unit_id:
                if config.log_register_queries:
                    logging.info(
                        "Modbus query ignored from %s: fc=%s unit=%s expected_unit=%s",
                        client,
                        function_code,
                        unit_id,
                        config.unit_id,
                    )
                continue

            if function_code not in {3, 4}:
                body = _exception(function_code, 0x01)
                if config.log_register_queries:
                    logging.info(
                        "Modbus query from %s: fc=%s unsupported",
                        client,
                        function_code,
                    )
            elif len(pdu) != 5:
                body = _exception(function_code, 0x03)
                if config.log_register_queries:
                    logging.info(
                        "Modbus query from %s: fc=%s invalid_pdu_length=%s",
                        client,
                        function_code,
                        len(pdu),
                    )
            else:
                start, quantity = struct.unpack(">HH", pdu[1:5])
                body = _build_read_response(function_code, start, quantity, state)
                if config.log_register_queries:
                    end = start + quantity - 1
                    logging.info(
                        "Modbus query from %s: fc=%s range=%s-%s qty=%s",
                        client,
                        function_code,
                        start,
                        end,
                        quantity,
                    )

            mbap = struct.pack(">HHHB", transaction_id, 0, len(body) + 1, unit_id)
            if config.log_protocol_debug:
                logging.info("Modbus response to %s: mbap=%s pdu=%s", client, mbap.hex(), body.hex())
            writer.write(mbap + body)
            await writer.drain()
    except asyncio.IncompleteReadError:
        if config.log_register_queries:
            logging.info("Modbus client read ended early: %s", client)
        pass
    finally:
        logging.info("Modbus client disconnected: %s", client)
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
