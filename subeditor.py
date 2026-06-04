"""
subeditor.py — Interactive Subtitle Sync Fixer
------------------------------------------------
An interactive CLI for fixing out-of-sync SRT subtitle files.

Run with:
    python subeditor.py
"""

import sys
from pathlib import Path
from fix_subs import fix_subtitles


def get_input_file() -> str:
    '''Get path to the SRT file.'''
    while True:
        input_path = Path(input('Enter file path to the SRT file: '))

        if not input_path.exists():
            print(f'Error: file not found: {input_path}')
            continue

        if input_path.suffix != '.srt':
            print(f'Error: file is not SRT: {input_path}')
            continue

        return str(input_path)


def get_direction() -> str:
    '''Determine the sync direction (advance or delay).'''
    print('STEP 2 — Sync Direction')
    print('-' * 50)
    while True:
        print('[A]  Subs appear TOO LATE  → advance them (move earlier)')
        print('[D]  Subs appear TOO EARLY → delay them  (move later)')
        choice = input('Your choice (A / D): ').lower()

        if choice not in ('a', 'd'):
            print(f'Invalid value for direction: {choice}')
            print('Try Again!\n')
            continue

        direction = 'delay' if choice == 'd' else 'advance'

        print(f'✓ Will {direction} the subtitles')
        return direction


def get_offset():
    pass


def get_output_option(input_file):
    pass


def run():
    get_input_file()
    direction = get_direction()


if __name__ == "__main__":
    run()
