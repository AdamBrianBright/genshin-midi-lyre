# Genshin MIDI Lyre
Play midi file on Windsong Lyre.

## Requirements

* Genshin Impact(原神) on Windows
* Python 3
* `keyboard` module
* `mido` module
* Git (optional)

## Install

```
git clone https://github.com/EHfive/genshin-midi-lyre.git
cd genshin-midi-lyre
pip install -r .\requirements.txt
```

## Usage

```
> python .\main.py --help
usage: main.py [-h] [-c [CHANNELS ...]] [-o OCTAVE] [--no-semi] [--shift] [midi]

Play midi file on Windsong Lyre in Genshin

positional arguments:
  midi                  path to midi file

optional arguments:
  -h, --help            show this help message and exit
  -c [CHANNELS ...], --channels [CHANNELS ...]
                        enabled midi channels
  -o OCTAVE, --octave OCTAVE
                        shift octave
  --no-semi             don't shift black key to white key
  --shift               shift notes which out of range
```

1. Start Genshin Impact(原神)
2. Equipt Windsong Lyre
3. Press Z (or your custom keymap) to use Windsong Lyre
4. Run `admin_cmd.bat` to get an administrator cmd terminal
5. Run `python main.py [path to midi file]` in administrator terminal

## Credits

"canon.mid" & "admin_cmd.bat" are borrowed from https://github.com/Misaka17032/genshin-lyre-auto-play