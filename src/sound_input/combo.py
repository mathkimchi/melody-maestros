import enum


class Tone(enum.Enum):
    LOW = 39
    F2 = 41
    FG2 = 42
    G2 = 43
    GA2 = 44
    A2 = 45
    AB2 = 46
    B2 = 47
    C3 = 48
    CD3 = 49
    D3 = 50
    DE3 = 51
    E3 = 52
    F3 = 53
    FG3 = 54
    G3 = 55
    GA3 = 56
    A3 = 57
    AB3 = 58
    B3 = 59
    C4 = 60
    CD4 = 61
    D4 = 62
    DE4 = 64
    E4 = 64
    F4 = 65
    FG4 = 66
    G4 = 67
    GA4 = 68
    A4 = 69
    AB4 = 70
    B4 = 71
    C5 = 72
    CD5 = 73
    D5 = 74
    DE5 = 75
    E5 = 76
    HIGH = 78
    # __order__ = "LOW F2 G2 A2 B2 C3 D3 E3 F3 G3 A3 B3 C4 D4 E4 F4 G4 A4 B4 C5 D5 E5 HIGH"


FAST_ATTACK = [  # 1
    Tone.C3.value,
    Tone.E3.value,
    Tone.F3.value,
]
RANGED_ATTACK = [  # 2
    Tone.C3.value,
    Tone.G3.value,
    Tone.C3.value,
]
STRONG_ATTACK = [
    Tone.C3.value,
    Tone.G3.value,
    Tone.F3.value,
    Tone.D3.value,
    Tone.E3.value,
]

MIN_HOLD_LEN = 5
BREAK_LEN = 20


def get_held_notes(all_notes):
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


def matches_combo(held_notes, combo) -> bool:
    return (len(held_notes) >= len(combo)) and combo == held_notes[-len(combo) :]


def find_matching_combo(notes) -> int:
    held_notes = get_held_notes(list(notes))
    if matches_combo(held_notes, FAST_ATTACK):
        return 1
    elif matches_combo(held_notes, RANGED_ATTACK):
        return 2
    else:
        return 0
