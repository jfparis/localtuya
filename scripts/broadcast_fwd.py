#!/usr/bin/python3

import asyncio
import argparse
import logging

_LOGGER = logging.getLogger(__name__)


class TuyaBroadcastFwder(asyncio.DatagramProtocol):
    """Datagram handler listening for Tuya broadcast messages."""

    def __init__(self, listening_port, dest_addr):
        """Initialize a new Fwder protocol."""
        self.listening_port = listening_port
        self.dest_addr = dest_addr
        self.transport = None
        self.listener = None

    def connection_made(self, transport):
        self.transport = transport

    def start(self, loop):
        """initiate the listener"""

        self.listener = loop.create_datagram_endpoint(
            lambda: self, local_addr=("0.0.0.0", self.listening_port)
        )
        loop.run_until_complete(self.listener)

        _LOGGER.debug(f"Listening to broadcasts on UDP port {self.listening_port}")

    def datagram_received(self, data, addr):
        """Handle received broadcast message."""
        _LOGGER.debug(f"Got datagram from {addr}")
        self.transport.sendto(data, self.dest_addr)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=
        "Python script that forward tuya UDP discovery broadcast to any given host. \n\n"
        "By default Tuya devices UDP broadcast will only be received by devices \n"
        "that are running on the same subnet. This could be a problem if you are \n"
        "segregating your IOT devices on an 'untrusted' network and running HASS \n"
        "your trusted network \n \n"
        "This forwarder script will forward the discovery packets to host where HASS \n"
        "is running. \n\n"
        "./braodcast_fwd.py [host]")
    parser.add_argument('--debug', help='debug mode', action="store_true")
    parser.add_argument('host', type=str, help="host where packets should be forwarded")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    tuya = TuyaBroadcastFwder(6666, (args.host, 6666))
    enc_tuya = TuyaBroadcastFwder(6667, (args.host, 6667))

    tuya.start(loop)
    enc_tuya.start(loop)

    loop.run_forever()


if __name__ == "__main__":
    main()
