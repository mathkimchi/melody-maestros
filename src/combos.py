import const
from const import Tone

FAST_ATTACK = [Tone.C3.value, Tone.E3.value, Tone.F3.value]
MIN_HOLD_LEN = 5
BREAK_LEN = 20


def held_notes(all_notes):
    reverse_all_notes = all_notes[::-1]
    reverse_held_notes = []

    index = 0
    unpattern_len = 0
    while index < len(reverse_all_notes):
        pattern_end_index = index + 1  # rev[pei] != rev[i]

        while pattern_end_index < len(reverse_all_notes):
            if reverse_all_notes[pattern_end_index] != reverse_all_notes[index]:
                break

            pattern_end_index += 1

        pattern_len = pattern_end_index - index

        if (pattern_len >= MIN_HOLD_LEN) and (
            Tone.LOW.value < reverse_all_notes[index]
        ):
            reverse_held_notes.append(reverse_all_notes[index])
            unpattern_len = 0
        else:
            unpattern_len += pattern_len

        if unpattern_len >= BREAK_LEN:
            break

        index = pattern_end_index

    return reverse_held_notes[::-1]


def matches_combo(held_notes, combo):
    return combo == held_notes


print(held_notes([0, 0, 0, 1, 2, 2, 2, 2, 2, 3, 4, 5, 6, 7, 4, 4, 4, 4, 4]))
