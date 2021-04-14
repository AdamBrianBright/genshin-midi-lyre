# Genshin MIDI Lyre

Play midi file with Windsong Lyre.

## Requirements

* Genshin Impact(原神) on Windows
* Python 3

## Automatic Install

- Download and extract .zip with this repo
- Run `setup.cmd` to automatically setup virtualenv and requirements
- Create shortcut to `run.cmd` and mark to **run as administrator**
- Put `.mid` files in `C:\your-path-to\genshin-midi-lyre\files` directory

## Automatic Usage

1. Start Genshin Impact(原神)
2. Equipt Windsong Lyre
3. Press Z (or your custom keymap) to use Windsong Lyre
4. Run `run.cmd` shortcut as administrator
6. Switch back to Genshin Impact window, press `\` to start/stop playing
7. Press `backspace` to exit

## Manual install

```
git clone https://github.com/AdamBrianBright/genshin-midi-lyre.git
cd genshin-midi-lyre
python -m virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Manual Usage

```
> python .\player.py --help
usage: player.py [-h] [-c [CHANNELS ...]] [-s SHIFT] [--no-semi] [--shift-out-of-range] [midi]

Play midi file with Windsong Lyre in Genshin Impact

positional arguments:
  midi                  path to midi file

optional arguments:
  -h, --help            show this help message and exit
  -c [CHANNELS ...], --channels [CHANNELS ...]
                        enabled midi channels, available values:0, 1, 2,...,N
  -s SHIFT, --shift SHIFT
                        shift note pitch, auto calculated by default
  --no-semi             don't shift black key to white key
  --shift-out-of-range  shift notes which out of range
```

## Credits

"canon.mid" & "admin_cmd.bat" are borrowed from https://github.com/Misaka17032/genshin-lyre-auto-play

Forked from: https://github.com/EHfive/genshin-midi-lyre

Changed functional approach to Class based

