# Melody Maestros

To play Melody Maestros (assuming linux or macos):
1. clone this repo (`git clone https://github.com/mathkimchi/melody-maestros`) and enter the directory (`cd melody-maestros`)
2. make a new virtual environment (venv) and activate it (`python -m venv venv`, `source venv/bin/activate`)
3. install `pygame`, `pyaudio` and `urllib3` (`pip install pygame pyaudio urllib3`)
4. install aubio: `git clone https://github.com/aubio/aubio`, `cd aubio`, `pip install -v .` with the virtual environment active
5. `cd ..`, you should be in the `melody-maestros` directory
6. `python src/client_runner.py`

Moves:
- FAST_ATTACK: C3
- RANGED_ATTACK: E3, G3, B2
- STRONG_ATTACK: G3, E3, G3
- FALL_ATTACK: G3, F3, E3
- JUMP_ATTACK: E3, F3, G3
- BLOCK: G2
