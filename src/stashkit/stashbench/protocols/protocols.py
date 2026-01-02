# protocols.py
"""
Protocol handler registry for StashBench.

Handlers are intentionally simple and mechanical.
"""

def http_json_handler(query_packet: dict) -> dict:
    connection = query_packet["connection"]
    endpoint = connection.get("endpoint")

    if not endpoint:
        raise ValueError("HTTP JSON handler requires connection.endpoint")

    inputs = query_packet.get("inputs", {})

    # Stubbed response for now
    return {
        "_meta": {
            "protocol": "http_json",
            "endpoint": endpoint,
        },
        "data": {
            "simulated": True,
            "inputs": inputs,
        }
    }


PROTOCOL_HANDLERS = {
    "http_json": http_json_handler,
}
