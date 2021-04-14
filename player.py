from dataclasses import dataclass
from os import listdir, path
from random import choice
from time import sleep
from typing import List, Optional

import keyboard as kbd
import mido


@dataclass
class Song:
    name: str
    midi: mido.MidiFile
    shift: int


BASE_DIR = path.dirname(__file__)
FILES_DIR = path.join(BASE_DIR, 'files')


class GenshinLyreMidiPlayer:
    __slots__ = ('songs', 'channels', 'state', 'no_semi', 'out_range',)
    octave_interval = 12

    c3_pitch = 48
    c4_pitch = 60
    c5_pitch = 72
    b5_pitch = 83
    KEY_TABLE = "z?x?cv?b?n?m" + "a?s?df?g?h?j" + "q?w?er?t?y?u"
    NOTE_TABLE = "C?D?EF?G?A?B"

    def __init__(self, channels: List[int], no_semi: bool, out_range: bool, midi: str = None):
        self.songs: List[Song] = []
        self.channels = channels
        self.state = 'idle'
        self.no_semi = no_semi
        self.out_range = out_range

        files = [midi] if midi else listdir(FILES_DIR)

        for file in files:
            file_path = path.join(FILES_DIR, file)
            if not path.isfile(file_path):
                continue
            try:
                midi_file = mido.MidiFile(file_path)
                shift = self.find_best_shift(midi_file)
                self.songs.append(Song(file, midi_file, shift))
            except KeyboardInterrupt:
                raise
            except (AttributeError, OSError, ValueError, KeyError, IndexError):
                print(f'Failed to load {file_path}, skipping')

    def start(self):
        kbd.add_hotkey('\\', self.control, suppress=True, trigger_on_release=True)
        self.show_help()
        kbd.wait('backspace', suppress=True)

    def msg_filter(self, msg, ch=None):
        if ch is None:
            ch = self.channels
        return self.midi_play_filter(msg, ch)

    def show_help(self):
        print('Press "\\" to start/stop playing, press "backspace" to exit.\n')

    def note_name(self, note):
        idx = note % self.octave_interval
        if idx < 0:
            return '-'
        pre = self.NOTE_TABLE[idx]
        if pre == '?':
            pre = self.NOTE_TABLE[idx - 1] + '#'
        return pre + str(note // self.octave_interval - 1)

    def print_note(self, ch, orig, play, key):
        print(f"ch {ch:<2}  orig: {self.note_name(orig):<3}{'(' + str(orig) + ')':<5}"
              f"  play: {self.note_name(play) if play else '-':<3}{'(' + str(play) + ')' if play else '-':<5}"
              f"    {key if key else '-'}\n")

    def get_random_song(self) -> Optional[Song]:
        if self.songs:
            return choice(self.songs)

    def play(self):
        self.state = 'running'
        song = self.get_random_song()
        if not song:
            return self.stop('Nothing to play')

        print(f'Start playing {song.name}')
        for msg in song.midi:
            if self.state != 'running':
                break

            sleep(msg.time)

            if not self.msg_filter(msg):
                continue

            note = msg.note + song.shift
            orig_note = note

            if note < self.c3_pitch:
                print(f'note {note:<3} lower than C3 : {self.c3_pitch - note:+}')
                if self.out_range:
                    note = note % self.octave_interval + self.c3_pitch
            elif note > self.b5_pitch:
                print(f'note {note:<3} higher than B5: {self.b5_pitch - note:+}')
                if self.out_range:
                    note = note % self.octave_interval + self.c5_pitch

            if note < self.c3_pitch or note > self.b5_pitch:
                self.print_note(msg.channel, orig_note, None, None)
                continue

            if self.KEY_TABLE[note - self.c3_pitch] == '?' and not self.no_semi:
                note -= 1
            key = self.KEY_TABLE[note - self.c3_pitch]
            self.print_note(msg.channel, orig_note, note, key.upper())
            kbd.send(key)

        self.stop()

    def stop(self, message: str = None):
        print(message or 'Stop playing')
        self.show_help()
        self.state = 'idle'

    def control(self):
        if self.state == 'running':
            self.state = 'stopping'
        elif self.state == 'idle':
            kbd.call_later(self.play, delay=1)

    def find_best_shift(self, midi_iter) -> int:
        count_list = [0] * self.octave_interval
        octave_list = [0] * 11
        for msg in midi_iter:
            if not self.msg_filter(msg):
                continue
            for i in range(self.octave_interval):
                note_pitch = (msg.note + i) % self.octave_interval
                if self.KEY_TABLE[note_pitch] != '?':
                    count_list[i] += 1
                    note_octave = (msg.note + i) // self.octave_interval
                    octave_list[note_octave] += 1
        idx = int(max(range(len(count_list)), key=count_list.__getitem__))
        idx2 = 0
        count = 0
        i = 0
        while i + 3 <= len(octave_list):
            tmp = sum(octave_list[i:i + 3])
            if tmp > count:
                count = tmp
                idx2 = i
            i += 1

        return idx + (4 - idx2) * self.octave_interval

    def midi_play_filter(self, msg, channels):
        if msg.is_meta or msg.type != 'note_on':
            return False
        if channels and msg.channel not in channels:
            return False
        return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Play midi file with Windsong Lyre in Genshin Impact')
    parser.add_argument('midi', nargs="?", type=str, help='Name of .mid file in "files" directory')
    parser.add_argument('-c', '--channels', nargs="*", type=int,
                        help="enabled midi channels, available values:0, 1, 2,...,N")
    parser.add_argument('-s', '--shift', type=int, default=None,
                        help="shift note pitch, auto calculated by default")
    parser.add_argument('-n', '--no-semi', action='store_true',
                        help="don't shift black key to white key")
    parser.add_argument('-r', '--shift-out-of-range', dest="out_range",
                        action='store_true', help="shift notes which out of range")
    args = parser.parse_args()

    player = GenshinLyreMidiPlayer(args.channels, args.no_semi, args.out_range, args.midi)
    player.start()
