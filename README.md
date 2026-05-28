# 🎬 Subeditor — Subtitle Sync Fixer

A simple Python script that fixes out-of-sync `.srt` subtitle files by shifting all timestamps forward or backward by a fixed amount.

---

## 📋 Requirements

- Python 3
- The `srt` library

Install the `srt` library with:

```bash
pip install srt
```

---

## 📁 File Setup

Place **both** the script and your subtitle file in the **same folder**:

```bash
📂 your-folder/
├── fix_subs.py
└── movie.srt
```

The corrected subtitle file will also be saved in the **same folder** automatically:

```bash
📂 your-folder/
├── fix_subs.py
├── movie.srt
└── movie_fixed.srt   ✅ new file
```

---

## 🚀 Usage

Open a terminal, navigate to the folder, and run:

```bash
python fix_subs.py <subtitle_file.srt> <offset_in_milliseconds>
```

The offset is in **milliseconds** — where 1 second = 1000 ms.

---

## 🔧 Examples

**Subs appear too early** (they show up before the actor speaks) → delay them with a positive number:

```bash
python fix_subs.py movie.srt 2500
```

> Shifts all subtitles 2.5 seconds later

**Subs appear too late** (the actor already spoke before they show up) → advance them with a negative number:

```bash
python fix_subs.py movie.srt -1800
```

> Shifts all subtitles 1.8 seconds earlier

---

## ⚠️ Known Limitations

- **Mal-formatted SRT files will likely throw an error.** SRT files downloaded from sites like OpenSubtitles sometimes have formatting inconsistencies that cause the `srt` library to crash during parsing. If this happens, try opening the `.srt` file in a text editor and checking for unusual characters or broken timestamp lines.

- This script applies a **single fixed offset** to all timestamps. If your subtitles start in sync but gradually drift out over time, a fixed offset won't fully solve the problem.

---

## 📄 License

Free to use and modify for personal use.
