"""
This is the file that actually runs Melody Maestros.
"""

from net.server import Server
from net.client import Client

if __name__ == "__main__":  # if this is the file being run
    Server().run()
    # Client(("localhost", 8080)).run()
