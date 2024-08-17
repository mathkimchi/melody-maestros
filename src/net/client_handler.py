from game.game_state import GameState
import pygame
import socket
import json
from game.player_actions import PlayerActionSet


class ClientHandler:
    """
    This can be thought of as the representation of the client on the server side.
    """

    def __init__(self, client_socket: socket.socket, server, player_id: int) -> None:
        self.client_socket = client_socket
        self.server = server
        self.player_id = player_id

    def run(self) -> None:
        # send initial messages for config
        self.client_socket.sendall(json.dumps(self.player_id).encode())

        while True:
            packet = PlayerActionSet(
                **json.loads(self.client_socket.recv(1024).decode())
            )

            self.server.process_packet(self, packet)
