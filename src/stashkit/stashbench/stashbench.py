# stashbench.py
"""
Minimal StashBench scaffold.

StashBench provides execution mechanics for data access.
It knows *how* to execute a query, not *what* it means.
"""

from .protocols.protocols import PROTOCOL_HANDLERS


class StashBench:
    class data:
        @staticmethod
        def connection(query_packet: dict):
            if not isinstance(query_packet, dict):
                raise TypeError("QueryPacket must be a dict-like object")

            connection = query_packet.get("connection")
            if not connection:
                raise ValueError("QueryPacket missing 'connection' section")

            protocol = connection.get("protocol")
            if not protocol:
                raise ValueError("QueryPacket missing connection.protocol")

            handler = PROTOCOL_HANDLERS.get(protocol)
            if not handler:
                raise NotImplementedError(
                    f"No handler registered for protocol '{protocol}'"
                )

            return handler(query_packet)
