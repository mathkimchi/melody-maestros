import pyaudio
import numpy as np
import aubio
import collections
from .combo import Tone, find_matching_combo, get_held_notes, Combo


PRINT_DBG = True

MIC_BUFFER_SIZE = 2048
MIC_SAMPLE_RATE = 48000

each_sample_time = MIC_BUFFER_SIZE / MIC_SAMPLE_RATE


note_list = list(Tone)


def find_note(val: float) -> Tone:
    """val in midi unit"""
    print(f"{val=}")
    rounded = max(Tone.LOW.value, min(int(round(val)), Tone.HIGH.value))
    print(f"{rounded=}")
    return Tone(rounded)


class ComboStream:
    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()

        self.pyaudio_format = pyaudio.paFloat32
        self.n_channels = 1
        self.stream = self.p.open(
            format=self.pyaudio_format,
            channels=self.n_channels,
            rate=MIC_SAMPLE_RATE,
            input=True,
            frames_per_buffer=MIC_BUFFER_SIZE,
        )

        self.tolerance = 0.8
        self.pitch_o = aubio.pitch(
            "default", 8192, MIC_BUFFER_SIZE, MIC_SAMPLE_RATE
        )  # type: ignore
        self.pitch_o.set_unit("midi")
        self.pitch_o.set_tolerance(self.tolerance)

    def get_combo_id(self) -> Combo:
        notes = collections.deque([0 for _ in range(200)])
        while True:
            audiobuffer = self.stream.read(MIC_BUFFER_SIZE, exception_on_overflow=False)
            signal = np.frombuffer(audiobuffer, dtype=np.float32)
            cur_pitch = find_note(self.pitch_o(signal)[0])

            if cur_pitch == Tone.LOW or cur_pitch == Tone.HIGH:
                notes.append(0)
            else:
                notes.append(cur_pitch.value)
            notes.popleft()

            if PRINT_DBG:
                print(f"{notes=}")
                print(f"{get_held_notes(list(notes))=}")

            combo = find_matching_combo(notes)
            if combo != None:
                # good thing about returning is that notes restart
                return combo
