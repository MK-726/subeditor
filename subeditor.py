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


SEPARATOR_SIZE = 80
HEADER_TEXT = 'SUBEDITOR - Subtitle Editor Tool'


def render_header(text: str = HEADER_TEXT) -> None:
    '''Render the CLI section header.'''
    padding = ((SEPARATOR_SIZE - len(text)) // 2) * ' '
    print()
    print('=' * SEPARATOR_SIZE)
    print(f'{padding}{text}')
    print('=' * SEPARATOR_SIZE)
    print()


def get_input_file() -> str:
    '''Get path to the SRT file.'''
    print('STEP 1 — Subtitle File')
    print('-' * SEPARATOR_SIZE)
    while True:
        print('Drag and drop your SRT file into this window,'
              ' or type the full path to it.')

        input_path = Path(input('Path: '))

        if not input_path.exists():
            print(f'Error: file not found: {input_path}')
            continue

        if input_path.suffix != '.srt':
            print(f'Error: file is not SRT: {input_path}')
            continue

        print(f' ✓  File found: {input_path}')
        return str(input_path)


def get_direction() -> str:
    '''Determine the sync direction (advance or delay).'''
    print('\nSTEP 2 — Sync Direction')
    print('-' * SEPARATOR_SIZE)
    while True:
        print('[A]  Subs appear TOO LATE  → advance them (move earlier)')
        print('[D]  Subs appear TOO EARLY → delay them  (move later)')
        choice = input('Your choice (A / D): ').lower()

        if choice not in ('a', 'd'):
            print(f'Invalid value for direction: {choice}')
            print('Try Again!\n')
            continue

        direction = 'delay' if choice == 'd' else 'advance'

        print(f'✓  Will {direction} the subtitles')
        return direction


def get_offset() -> int:
    '''Get offset in ms.'''
    print('\nSTEP 3 — Offset Amount')
    print('-' * SEPARATOR_SIZE)
    while True:
        try:
            offset = int(input('Enter offset in ms: '))
            if offset <= 0:
                print('Offset must be a positive number.')
                print('Try Again.\n')
                continue
            print(f'✓  Offset: {offset:,} ms ({offset / 1000:.2f} seconds)')
            return offset
        except ValueError:
            print('Offset must be a whole number (e.g. 1800).')
            print('Try Again.\n')


def get_output_option(input_file: str) -> str:
    '''Get output file path.'''
    print('\nSTEP 4 — Output File')
    print('-' * SEPARATOR_SIZE)
    print('Where should the corrected file be saved?')
    input_path = Path(input_file)

    while True:
        print('[R]  Replace the original file')
        print('[N]  Save as a new file')
        choice = input('Your choice (R / N): ').lower()

        if choice not in ('r', 'n'):
            print(f'Invalid choice: {choice}')
            print('Try Again!\n')
            continue

        if choice == 'r':
            print(f'✓  Will overwrite: {input_path.name}')
            return str(input_path)

        default = str(input_path.with_stem(input_path.stem + '_fixed'))
        print(f'Suggested name: {default}')
        custom = input(
            'Press Enter to use suggestion or type a custom path: ').strip()
        output_path = custom if custom else default
        print(f'✓  Will save to: {output_path}')
        return output_path


def render_summary(
    input_file: str, direction: str, offset: int, output: str
) -> None:
    '''Render the summary.'''
    render_header(text='SUMMARY')
    render_summary_info(input_file, direction, offset, output)


def render_summary_info(
        input_file: str, direction: str, offset: int, output: str
) -> None:
    '''Render the summary info.'''
    print(f'File   : {input_file}')
    print(
        f'Action : {direction.title()} by {offset:,}ms ({offset / 1000:.2f}s)'
    )
    print(f'Output : {output}')


def run():
    '''Run the interactive CLI.'''
    render_header()
    input_file = get_input_file()
    direction = get_direction()
    offset = get_offset()
    output = get_output_option(input_file)
    render_summary(input_file, direction, offset, output)
    signed_offset = offset if direction == 'delay' else -offset


if __name__ == "__main__":
    run()
