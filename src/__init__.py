"""
This is the file that actually runs Melody Maestros.
"""

from net.server import Server
from net.client import Client
import threading
import time

if __name__ == "__main__":  # if this is the file being run
    server = Server()
    threading.Thread(target=server.run).start()
    print("Started server")

    # time.sleep(1)

    # client0 = Client(("localhost", 8080))
    # threading.Thread(target=client0.run).start()
    # print("Started client 0")

    # client1 = Client(("localhost", 8080))
    # threading.Thread(target=client1.run).start()
    # print("Started client 1")