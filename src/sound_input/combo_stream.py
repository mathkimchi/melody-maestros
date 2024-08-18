import pyaudio
import numpy as np
import aubio
import collections
from .combo import Tone, find_matching_combo, get_held_notes, Combo


PRINT_DBG = False

MIC_BUFFER_SIZE = 2048
MIC_SAMPLE_RATE = 48000


def find_note(val: float) -> Tone:
    # aubio returns a float for pitch, we want integer
    # round, anything too low becomes Tone.LOW and same for high
    print(f"{val=}")
    rounded = max(Tone.LOW.value, min(int(round(val)), Tone.HIGH.value))
    print(f"{rounded=}")
    return Tone(rounded)


class ComboStream:
    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()

        # ritual to enable pyaudio microphone reading
        self.pyaudio_format = pyaudio.paFloat32
        self.n_channels = 1
        self.stream = self.p.open(
            format=self.pyaudio_format,
            channels=self.n_channels,
            rate=MIC_SAMPLE_RATE,
            input=True,
            frames_per_buffer=MIC_BUFFER_SIZE,
        )

        # ritual to start aubio pitch detection
        # it was better than anything we could make ourselves with numpy FFTs
        self.tolerance = 0.8
        self.pitch_o = aubio.pitch(
            "default", 8192, MIC_BUFFER_SIZE, MIC_SAMPLE_RATE
        )  # type: ignore
        self.pitch_o.set_unit("midi")
        self.pitch_o.set_tolerance(self.tolerance)

    def get_combo_id(self) -> Combo:
        # notes is a 200 entry deque
        notes = collections.deque([0 for _ in range(200)])
        while True:
            # read microphone from pyaudio
            audiobuffer = self.stream.read(
                MIC_BUFFER_SIZE, exception_on_overflow=False)
            signal = np.frombuffer(audiobuffer, dtype=np.float32)
            cur_pitch = find_note(self.pitch_o(signal)[0])

            # add one and remove one to limit length to 200
            # to avoid performance problems when playing for too long
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
