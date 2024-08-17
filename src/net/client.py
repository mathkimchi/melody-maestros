from game.game_state import GameState
from game.player_actions import PlayerActionSet
import pygame
import sys
import socket
import json
from dataclasses import asdict
from .socket_input_stream import SocketInputStream


class Client:
    def __init__(self, server_address) -> None:
        # initial comminication with client handler
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(server_address)
        self.socket_input_stream = SocketInputStream(self.server_socket, auto_start=True)
        self.player_id: int = self.socket_input_stream.get_object()
        print(f"Client recieved initial message: {self.player_id}")
        # The client GS is just an imitation of the server gs
        # content at this point doesn't matter, it will be replaced
        self.gs = GameState()

        # initiate display stuff
        pygame.init()
        pygame.display.set_caption("Client View")
        self.screen = pygame.display.set_mode((540, 540))
        self.clock = pygame.time.Clock()
        self.continue_running = True

    def run(self) -> None:
        while self.continue_running:
            for event in pygame.event.get():
                # exit handle
                if event.type == pygame.QUIT:
                    sys.exit()

            # # The client GS is just an imitation of the server gs
            self.gs.parse_json_in_place(self.socket_input_stream.get_object())

            # ---
            # Display

            # reset display
            self.screen.fill((0, 0, 0))

            self.gs.draw(surface=self.screen)

            # NOTE changes don't show until this is called
            pygame.display.update()
            # ---

            self.handle_inputs()

    def handle_inputs(self) -> None:
        # start with default (no actions)
        action_set = PlayerActionSet(0, False, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] == True:
            action_set.walk_direction = -1
        elif pressed_keys[pygame.K_RIGHT] == True:
            action_set.walk_direction = +1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # only called on button down, not constantly
                clicked_key: int = event.key
                if clicked_key == pygame.K_UP:
                    action_set.jump = True
                if clicked_key == pygame.K_LSHIFT:
                    action_set.attack = 1

        # print(f"Sending: {json.dumps(asdict(action_set))=}")
        self.server_socket.sendall((json.dumps(asdict(action_set))+"\n").encode())
