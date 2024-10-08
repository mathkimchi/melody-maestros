from game.game_state import GameState
from game.player_actions import PlayerActionSet
import pygame
import pygame.font
import sys
import socket
import json
from dataclasses import asdict
from .socket_input_stream import SocketInputStream
from sound_input.sound_events import SoundEventQueue
from sound_input.combo import Combo

ALLOW_KEYBOARD_ATTACKS = True
PLAY_MUSIC = False


class Client:
    def __init__(self, server_address) -> None:
        # initial comminication with client handler
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(server_address)
        self.socket_input_stream = SocketInputStream(
            self.server_socket, auto_start=True
        )
        self.player_id: int = self.socket_input_stream.get_object()
        print(f"Client recieved initial message: {self.player_id}")
        # The client GS is just an imitation of the server gs
        # content at this point doesn't matter, it will be replaced
        self.gs = GameState()

        # initiate display stuff
        pygame.init()
        pygame.display.set_caption("Client View")
        self.screen = pygame.display.set_mode((1200, 600))
        self.clock = pygame.time.Clock()
        self.continue_running = True

        # things to display when player dies
        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans MS", 36)
        self.die_text = font.render("You died!", False, (0, 0, 0))
        self.die_overlay = pygame.Surface((1200, 600), pygame.SRCALPHA)
        self.die_overlay.fill((255, 0, 0, 30))

    def run(self) -> None:
        if PLAY_MUSIC:
            pygame.mixer.init()
            music = pygame.mixer.Sound("assets/soundtrack/fight.mp3")
            # trim bc musescore exports with an end pause, theoretically exact but is still weird
            music_raw = music.get_raw()
            music_raw = music_raw[
                : int((len(music_raw) / music.get_length()) * 60 / 170 * 8 * 4)
            ]
            music = pygame.mixer.Sound(music_raw)
            music.play(-1)

        self.sound_event_queue = SoundEventQueue()

        while self.continue_running:
            for event in pygame.event.get():
                # exit handle
                if event.type == pygame.QUIT:
                    sys.exit()

            # # The client GS is just an imitation of the server gs
            self.gs.parse_json_in_place(self.socket_input_stream.get_object())
            # reset and draw
            self.screen.fill((255, 255, 255))
            self.gs.draw(surface=self.screen)

            # server will remove player from list of players when they die
            # if current player is not there, player is dead and show overlay
            players = self.gs.players
            if str(self.player_id) not in players:
                self.screen.blit(self.die_text, (16, 16))
                self.screen.blit(self.die_overlay, (0, 0))

            pygame.display.update()
            self.handle_inputs()

    def handle_inputs(self) -> None:
        # start with default (no actions)
        action_set = PlayerActionSet(0, False, None)

        pressed_keys = pygame.key.get_pressed()

        # handle movement
        if pressed_keys[pygame.K_LEFT]:
            action_set.walk_direction = -1
        elif pressed_keys[pygame.K_RIGHT]:
            action_set.walk_direction = +1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # only called on button down, not constantly
                clicked_key: int = event.key
                if clicked_key == pygame.K_UP:
                    action_set.jump = True
                if ALLOW_KEYBOARD_ATTACKS:
                    if clicked_key == pygame.K_1:
                        action_set.combo = Combo(1)
                    if clicked_key == pygame.K_2:
                        action_set.combo = Combo(2)
                    if clicked_key == pygame.K_3:
                        action_set.combo = Combo(3)
                    if clicked_key == pygame.K_4:
                        action_set.combo = Combo(4)
                    if clicked_key == pygame.K_5:
                        action_set.combo = Combo(5)
                    if clicked_key == pygame.K_6:
                        action_set.combo = Combo(6)

        # handle sound
        for sound_event in self.sound_event_queue.get_combos():
            print(sound_event)
            action_set.combo = sound_event

        self.server_socket.sendall(
            (json.dumps(action_set.toJsonObj()) + "\n").encode())
