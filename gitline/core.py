import os
import subprocess
from collections import defaultdict
from gitline.languages import detect_language, detect_shebang, is_binary


def get_git_files(path):
    """Get all tracked files in a git repo via git ls-files."""
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return [os.path.join(path, f) for f in result.stdout.splitlines()]
    except Exception:
        pass
    return None


def get_all_files(path):
    """Walk directory and return all files (excluding .git)."""
    files = []
    for root, dirs, names in os.walk(path):
        # Skip hidden dirs and .git
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in names:
            if name.startswith("."):
                continue
            files.append(os.path.join(root, name))
    return files


def count_lines(filepath):
    """Count lines in a file efficiently."""
    try:
        with open(filepath, "rb") as f:
            buf = f.read(65536)
            if not buf:
                return 0
            count = buf.count(b"\n")
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                count += chunk.count(b"\n")
            return count
    except Exception:
        return 0


def count_file(filepath, extensions, shebangers):
    """Count lines for a single file, return (language, lines, is_match)."""
    _, ext = os.path.splitext(filepath)
    basename = os.path.basename(filepath)

    lang = None

    # Try extension/filename map first
    if ext:
        lang = extensions.get(ext.lower())
    if not lang:
        lang = extensions.get(basename)

    # Try shebang
    if not lang:
        try:
            with open(filepath, "rb") as f:
                first = f.read(128)
                if first.startswith(b"#!"):
                    for pattern, l in shebangers:
                        if pattern in first:
                            lang = l
                            break
        except Exception:
            pass

    # Skip if no language detected
    if not lang:
        return None, 0, False

    lines = count_lines(filepath)
    return lang, lines, True


def analyze(path, verbose=False):
    """Analyze a path and return language stats."""
    files = get_git_files(path)
    if files is None:
        if verbose:
            print("  Not a git repo, scanning filesystem...")
        files = get_all_files(path)

    stats = defaultdict(int)
    by_file = []
    skipped = 0
    binary_skipped = 0
    unknown = 0

    for fp in files:
        if not os.path.isfile(fp):
            continue

        if is_binary(fp):
            binary_skipped += 1
            continue

        _, ext = os.path.splitext(fp)
        basename = os.path.basename(fp)

        lang = detect_language(fp, ext)

        # Try shebang
        if not lang:
            try:
                with open(fp, "rb") as f:
                    first = f.read(128)
                    if first.startswith(b"#!"):
                        lang = detect_shebang(first)
            except Exception:
                pass

        if not lang:
            unknown += 1
            continue

        lines = count_lines(fp)
        stats[lang] += lines
        by_file.append((fp, lang, lines))

        if verbose:
            print(f"  {lang:<15} {lines:>8}  {fp}")

    return {
        "stats": dict(stats),
        "total": sum(stats.values()),
        "files": len(by_file),
        "skipped": skipped,
        "binary_skipped": binary_skipped,
        "unknown": unknown,
        "by_file": by_file if verbose else [],
    }


def diff_between(ref_a="main", ref_b="HEAD", path="."):
    """Count lines added/deleted between two refs."""
    try:
        result = subprocess.run(
            ["git", "diff", "--stat", ref_a, ref_b],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout.strip()
    except Exception:
        return "Error running git diff"
