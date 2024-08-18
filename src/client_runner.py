"""
Runs just the client.
"""

from net.client import Client
import urllib3

GET_URL_LOCALLY = False

if __name__ == "__main__":  # if this is the file being run
    # addr = input("Server IP: ")

    # port = input("Port: ")
    # if port == "":
    #     print("Defaulting to 8080.")
    #     port = 8010
    # else:
    #     port = int(port)

    Client(("0.0.0.0", 8080)).run()

    # if GET_URL_LOCALLY:
    #     with open("server_url.txt") as file:
    #         data = file.read()
    # else:
    #     http = urllib3.PoolManager()
    #     response = http.request(
    #         "GET",
    #         "https://raw.githubusercontent.com/mathkimchi/melody-maestros/master/server_url.txt",
    #     )
    #     data = response.data.decode("utf-8")

    # data = data.split("\n")
    # url = data[0]
    # port = int(data[1])

    # print(f"connect to server: {url}:{port}")

    # Client((url, int(port))).run()
