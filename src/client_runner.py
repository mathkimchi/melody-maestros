"""
Runs just the client.
"""

from net.client import Client

if __name__ == "__main__":  # if this is the file being run
    addr = input("Server IP: ")

    port = input("Port: ")
    if port == "":
        print("Defaulting to 8080.")
        port = 8080
    else:
        port = int(port)

    Client((addr, port)).run()
