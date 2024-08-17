from game.game_state import GameState
import pygame
import socket
import json
from game.player_actions import PlayerActionSet
import threading
from .socket_input_stream import SocketInputStream


class ClientHandler:
    """
    This can be thought of as the representation of the client on the server side.
    """

    def __init__(self, client_socket: socket.socket, server, player_id: int, auto_start=False) -> None:
        self.client_socket = client_socket
        self.server = server
        self.player_id = player_id

        # send initial messages for config
        self.client_socket.sendall((json.dumps(self.player_id)+"\n").encode())

        if auto_start:
            threading.Thread(target=self.run_recv_loop).start()

    def run_recv_loop(self) -> None:
        recv_stream = SocketInputStream(connection_socket=self.client_socket, auto_start=True)
        while True:            
            packet = PlayerActionSet(**recv_stream.get_object())

            self.server.process_packet(self, packet)

    def update_client_gs(self, packet: str):
        """Send an updated version of the game state to the client."""
        try:
            self.client_socket.sendall((packet+"\n").encode())
        except BrokenPipeError:
            pass
