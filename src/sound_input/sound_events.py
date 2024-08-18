from .combo_stream import ComboStream
from .combo import Combo
import threading


class SoundEventQueue:
    """
    Difference is that this doesn't require waiting until check.
    Similar to pygame's event keydown check.
    """

    def __init__(self) -> None:
        self.cs = ComboStream()
        self.event_queue: list[Combo] = []
        # make a new thread for audio listening
        # can't run in main loop because this is very time-sensitive
        threading.Thread(target=self.collect_combos_loop).start()

    def collect_combos_loop(self):
        while True:
            combo = self.cs.get_combo_id()
            self.event_queue.append(combo)

    def get_combos(self) -> list[Combo]:
        event_queue = self.event_queue
        self.event_queue = []
        return event_queue
