"""
Runs just the server.
"""

from net.server import Server
import socket

if __name__ == "__main__":  # if this is the file being run
    if input("Show IP?: ") == "y":
        print(f"Host Name: {socket.gethostname()}")
        print(f"IP: {socket.gethostbyname(socket.gethostname())}")
        print(f"FQDN: {socket.getfqdn()}")

    port = input("Port: ")
    if port == "":
        print("Defaulting to 8080.")
        port = 8080
    else:
        port = int(port)

    Server(("0.0.0.0", port)).run()
