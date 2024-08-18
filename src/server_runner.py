"""
Runs just the server.
"""

from net.server import Server
import socket

if __name__ == "__main__":
    # run on localhost:8080 and then use ngrok to port forward
    # so other people can connect to the server
    Server(("0.0.0.0", 8080)).run()
