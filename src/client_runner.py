"""
Runs just the client.
"""

from net.client import Client
import urllib3

if __name__ == "__main__":
    # ngrok (port forwarding service) changes the url and port when restarted
    # this file needs to know what that new port is
    # we make a file in the repo with the url and port, it is read here
    http = urllib3.PoolManager()
    response = http.request(
        "GET",
        "https://raw.githubusercontent.com/mathkimchi/melody-maestros/master/server_url.txt",
    )
    data = response.data.decode("utf-8")

    # first line is url, second line is port
    data = data.split("\n")
    url = data[0]
    port = int(data[1])

    print(f"connect to server: {url}:{port}")
    Client((url, int(port))).run()
