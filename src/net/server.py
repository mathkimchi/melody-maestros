import json
from game.game_state import GameState
from game.player_actions import PlayerActionSet
from .client_handler import ClientHandler
import pygame
import sys
import socket
import threading
from game.fighters.violinist import Violinist

MAX_FRAME_RATE = 30
SERVER_SIDE_DISPLAY = True


class Server:
    def __init__(self, port=8080) -> None:
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.gs = GameState()
        self.client_handlers: list[ClientHandler] = []

        self.id_counter = 0

    def run(self) -> None:
        self.serversocket.bind(("localhost", self.port))

        if SERVER_SIDE_DISPLAY:
            pygame.init()
            pygame.display.set_caption("Server View")
            self.screen = pygame.display.set_mode((540, 540))
        self.clock = pygame.time.Clock()

        self.continue_running = True

        client_accept_thread = threading.Thread(target=self.client_accept_loop)
        client_accept_thread.start()

        while self.continue_running:
            if SERVER_SIDE_DISPLAY:
                for event in pygame.event.get():
                    # exit handle
                    if event.type == pygame.QUIT:
                        self.continue_running = False
                        self.serversocket.close()
                        sys.exit()

                # ---
                # Display

                # reset display
                self.screen.fill((0, 0, 0))

                self.gs.draw(surface=self.screen)

                # NOTE changes don't show until this is called
                pygame.display.update()

            # in seconds
            delta_time = self.clock.tick(MAX_FRAME_RATE) / 1000.0

            self.gs.tick(delta_time)

            # serialize gs and update all clients
            packet = json.dumps(self.gs.toJsonObj()).encode()
            for client_handler in self.client_handlers:
                client_handler.update_client_gs(packet)

        # close everything
        self.serversocket.close()

    def client_accept_loop(self):
        self.serversocket.listen()
        while self.continue_running:
            conn, addr = self.serversocket.accept()

            print(f"New client from: {addr=}")

            self.gs.players[self.id_counter] = Violinist(self.gs)
            client_handler = ClientHandler(conn, self, self.id_counter)
            client_handler_thread = threading.Thread(target=client_handler.run)
            client_handler_thread.start()

            import time

            time.sleep(
                0.1
            )  # sometimes client handler sends multiple message when it shouldn't at the start

            self.client_handlers.append(client_handler)
            self.id_counter += 1

    def process_packet(self, client_handler: ClientHandler, packet: PlayerActionSet):
        """Handles packet from client to server. Currentlym packets are just action sets"""

        self.gs.players[client_handler.player_id].process_action_set(packet)
