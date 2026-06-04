# 🎬 Subeditor — Subtitle Sync Fixer

A simple Python script that fixes out-of-sync `.srt` subtitle files by shifting all timestamps forward or backward by a fixed amount.

---

## 📋 Requirements

- Python 3.7 or higher
- The `srt` library

**Using pipenv:**

```bash
pipenv install
```

**Using pip:**

```bash
pip install -r requirements.txt
```

**Or install directly:**

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

## ❌ Error Handling

The script will exit with a clear message if:

- The file does not exist
- The file is not an SRT file
- The file is empty or contains no valid subtitles
- The offset is larger than the first subtitle's start time

---

## ⚠️ Known Limitations

- **Malformed SRT blocks are silently skipped.** SRT files downloaded from sites like OpenSubtitles sometimes have formatting inconsistencies. The script will skip any malformed blocks and process the rest of the file.
- **Single fixed offset only.** If your subtitles start in sync but gradually drift out over time, a fixed offset won't fully solve the problem.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
