from game.game_state import GameState
from .client_handler import ClientHandler
import pygame
import sys
import socket
import threading

MAX_FRAME_RATE = 30
SERVER_SIDE_DISPLAY = True


class Server:
    def __init__(self, port=8080) -> None:
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.gs = GameState()
        self.client_handlers = []

    def run(self) -> None:
        self.serversocket.bind(("localhost", self.port))

        if SERVER_SIDE_DISPLAY:
            pygame.init()
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

        # close everything
        self.serversocket.close()

    def client_accept_loop(self):
        self.serversocket.listen()
        while self.continue_running:
            conn, addr = self.serversocket.accept()

            print(f"New client from: {addr=}")

            client_handler = ClientHandler(conn, self, 0)
            client_handler_thread = threading.Thread(target=client_handler.run)
            client_handler_thread.start()
            self.client_handlers.append(client_handler)
