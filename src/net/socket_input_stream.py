"""
TCP does not differentiate between messages, so if I wanted to send "1" and "2", it might send it as "12", if they are sent in quick succession.

To prevent this, I will be making this class which handles seperation and parsing.
"""

import json
import socket
import threading

class SocketInputStream:
    def __init__(self, connection_socket: socket.socket, auto_start=False) -> None:
        self.connection_socket = connection_socket
        self.objects_queue = []

        if auto_start:
            threading.Thread(target=self.run_input_loop).start()

    def run_input_loop(self):
        leftover_packet_str = ""
        while True:
            packets_str = leftover_packet_str+self.connection_socket.recv(1024).decode()

            split_packets = packets_str.split("\n")

            leftover_packet_str = split_packets.pop()

            for packet_str in split_packets:
                self.objects_queue.append(json.loads(packet_str))

    def get_object(self):
        while len(self.objects_queue)==0:
            import time
            time.sleep(0.01)

        return self.objects_queue.pop(0)
