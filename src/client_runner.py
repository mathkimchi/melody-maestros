"""
Runs just the client.
"""

from net.client import Client

if __name__ == "__main__":  # if this is the file being run
    Client(("localhost", 8080)).run()
