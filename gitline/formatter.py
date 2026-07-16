RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[38;5;245m"

RED = "\033[91m"

LANG_COLORS = {
    "Python": BLUE, "JavaScript": YELLOW, "TypeScript": BLUE,
    "Go": CYAN, "Rust": MAGENTA, "Java": MAGENTA,
    "C": BLUE, "C++": BLUE, "C#": GREEN,
    "Ruby": RED, "PHP": MAGENTA, "Shell": GREEN,
    "HTML": YELLOW, "CSS": BLUE, "SQL": MAGENTA,
    "Kotlin": MAGENTA, "Swift": MAGENTA, "Dart": BLUE,
    "Scala": RED, "Haskell": MAGENTA,
}



def bar(length, max_len, total, label="", color=""):
    width = 40
    bar_len = max(1, int(length / max(max_len, 1) * width))
    bar = "█" * bar_len
    pct = f"{(length / max(total, 1)) * 100:5.1f}%"
    return f" {color}{bar:<{width}}{RESET} {pct}"


def fmt_report(stats, total_files=None):
    lines = []
    items = sorted(stats.items(), key=lambda x: -x[1])
    max_lines = items[0][1] if items else 1
    total = sum(v for _, v in items)

    lines.append(f"\n  {BOLD}Language Breakdown{RESET}")
    lines.append(f"  {'─' * 60}")

    for lang, count in items:
        color = LANG_COLORS.get(lang, WHITE)
        pct = f"{(count / max(total, 1)) * 100:5.1f}"
        lines.append(
            f"  {color}{lang:<16}{RESET} "
            f"{count:>10,}  "
            f"{bar(count, max_lines, total)}"
        )

    lines.append(f"  {'─' * 60}")
    lines.append(f"  {BOLD}{'Total':<16}{RESET} {total:>10,}")
    if total_files is not None:
        lines.append(f"  {GRAY}Files: {total_files}{RESET}")

    return "\n".join(lines)


def fmt_json(stats, total_files=None, meta=None):
    import json
    return json.dumps({
        "languages": {k: v for k, v in sorted(stats.items(), key=lambda x: -x[1])},
        "total": sum(stats.values()),
        "files": total_files,
        **(meta or {}),
    }, indent=2)


def fmt_csv(stats, total_files=None):
    lines = ["Language,Lines"]
    for lang, count in sorted(stats.items(), key=lambda x: -x[1]):
        lines.append(f"{lang},{count}")
    lines.append(f"Total,{sum(stats.values())}")
    if total_files is not None:
        lines.append(f"Files,{total_files}")
    return "\n".join(lines)
