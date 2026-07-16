# gitline 📊

Count lines of code per language — pure Python, no external dependencies.

## Fitur

- **git-aware** — pake `git ls-files` untuk repo, fallback ke filesystem scan
- **80+ languages** — extension + shebang detection
- **Binary detection** — skip file binary otomatis
- **Multiple output** — human (ASCII bar), JSON, CSV
- **Diff mode** — statistik perubahan antar branch
- **Verbose per-file** — breakdown tiap file
- **Zero dependencies** — stdlib Python aja

## Instalasi

```bash
chmod +x install.sh
./install.sh
```

Pastikan `~/.local/bin` ada di PATH.

## Usage

```bash
gitline                          # Count current directory
gitline /path/to/project         # Count specific path
gitline --format json            # JSON output
gitline --format csv             # CSV output
gitline --verbose                # Per-file breakdown

gitline diff main HEAD           # Diff between branches
gitline files                    # List tracked files
gitline languages                # List supported languages
```

## Output

```
  Language Breakdown
  ────────────────────────────────────────────────────────────
  Python           797   ████████████████████████████████████████  85.1%
  Markdown         119   █████                                   12.7%
  Shell             20   █                                        2.1%
  ────────────────────────────────────────────────────────────
  Total            936
  Files: 12
```

## Tech Stack

- Python 3.12+ — stdlib only
- Git integration via `git ls-files`
- Binary detection via null byte scan
- Shebang detection for scripts without extension

## Struktur Project

```
gitline/
├── gitline/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py         # Argparse + command handlers
│   ├── core.py        # Line counting engine
│   ├── languages.py   # Extension/lang map + shebang detection
│   └── formatter.py   # Output formatting (human/JSON/CSV)
├── install.sh
└── README.md
```
