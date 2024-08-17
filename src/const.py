import enum
import dataclasses

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

@dataclasses.dataclass
class Note:
    tone: Tone
    time: float # seconds

FAST_ATTACK = [
    Note(Tone.C3, 0.3),
    Note(Tone.E3, 0.3),
    Note(Tone.F3, 0.3),
]
STRONG_ATTACK = [
    Note(Tone.C3, 0.3),
    Note(Tone.G3, 0.3),
    Note(Tone.F3, 0.3),
    Note(Tone.D3, 0.3),
    Note(Tone.E3, 0.3),
]

FAST_ATTACK_MAX_PCT = 0.25
STRONG_ATTACK_MAX_PCT = 0.3

MIC_BUFFER_SIZE = 2048
MIC_SAMPLE_RATE = 48000
# MIC_SAMPLE_RATE = 44100
