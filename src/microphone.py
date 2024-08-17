import pyaudio
import numpy as np
import aubio
import collections
import wgnfsh
import const
import combos

import os

each_sample_time = const.MIC_BUFFER_SIZE / const.MIC_SAMPLE_RATE

fast_attack: list[const.Tone] = []
strong_attack: list[const.Tone] = []
for note in const.FAST_ATTACK:
    fast_attack.extend([note.tone.value] * round(note.time / each_sample_time))
for note in const.STRONG_ATTACK:
    strong_attack.extend([note.tone.value] * round(note.time / each_sample_time))

print(strong_attack)

note_list = list(const.Tone)


def find_note(val: float) -> const.Tone:
    lo, hi = 0, len(note_list) - 1
    best_ind = lo
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if note_list[mid].value < val:
            lo = mid + 1
        elif note_list[mid].value > val:
            hi = mid - 1
        else:
            best_ind = mid
            break
        # check if data[mid] is closer to val than data[best_ind]
        if abs(note_list[mid].value - val) < abs(note_list[best_ind].value - val):
            best_ind = mid
    return note_list[best_ind]


p = pyaudio.PyAudio()

pyaudio_format = pyaudio.paFloat32
n_channels = 1
stream = p.open(
    format=pyaudio_format,
    channels=n_channels,
    rate=const.MIC_SAMPLE_RATE,
    input=True,
    frames_per_buffer=const.MIC_BUFFER_SIZE,
)

tolerance = 0.8
pitch_o = aubio.pitch("default", 8192, const.MIC_BUFFER_SIZE, const.MIC_SAMPLE_RATE)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

os.system("clear")

notes = collections.deque([0 for _ in range(200)])
while True:
    audiobuffer = stream.read(const.MIC_BUFFER_SIZE, exception_on_overflow=False)
    signal = np.frombuffer(audiobuffer, dtype=np.float32)
    cur_pitch = find_note(pitch_o(signal)[0])

    if cur_pitch == const.Tone.LOW or cur_pitch == const.Tone.HIGH:
        notes.append(0)
    else:
        notes.append(cur_pitch.value)
    notes.popleft()

    print(notes)
    print(combos.FAST_ATTACK)
    print(combos.held_notes(list(notes)))
    print(str(cur_pitch))
    # sys.stdout.flush()

    if combos.matches_combo(combos.held_notes(list(notes)), combos.FAST_ATTACK):
        print("FASTATTACK")

        import time

        time.sleep(1.0)

    fast_attack_match, fast_attack_dist = wgnfsh.match(
        list(notes), fast_attack, const.FAST_ATTACK_MAX_PCT
    )
    if fast_attack_match != -1:
        for _ in range(fast_attack_match):
            notes.pop()
            notes.appendleft(0)
        print(f"\r               \rFast attack, accuracy {fast_attack_dist:.2f}")

    strong_attack_match, strong_attack_dist = wgnfsh.match(
        list(notes), strong_attack, const.STRONG_ATTACK_MAX_PCT
    )
    if strong_attack_match != -1:
        for _ in range(strong_attack_match):
            notes.pop()
            notes.appendleft(0)
        print(f"\r               \rStrong attack, accuracy {strong_attack_dist:.2f}")

# stream.stop_stream()
# stream.close()
# p.terminate()
