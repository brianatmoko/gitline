import argparse
import os
import sys
from gitline import core, formatter as fmt


def cmd_count(args):
    path = args.path or "."
    path = os.path.abspath(path)

    if not os.path.exists(path):
        print(f"  {fmt.RED}✕ Path not found: {path}{fmt.RESET}")
        sys.exit(1)

    result = core.analyze(path, verbose=args.verbose)

    if args.format == "json":
        print(fmt.fmt_json(result["stats"], result["files"]))
    elif args.format == "csv":
        print(fmt.fmt_csv(result["stats"], result["files"]))
    else:
        print(fmt.fmt_report(result["stats"], result["files"]))

    extras = []
    if result["binary_skipped"]:
        extras.append(f"skipped {result['binary_skipped']} binary files")
    if result["unknown"]:
        extras.append(f"{result['unknown']} {'files' if result['unknown'] != 1 else 'file'} with unknown language")
    if extras:
        print(f"  {fmt.GRAY}({'; '.join(extras)}){fmt.RESET}", file=sys.stderr)


def cmd_diff(args):
    ref_a = args.base
    ref_b = args.head
    path = args.path or "."

    output = core.diff_between(ref_a, ref_b, path)
    print(output)


def cmd_list_files(args):
    path = args.path or "."
    path = os.path.abspath(path)

    files = core.get_git_files(path)
    if files is None:
        print(f"  {fmt.RED}Not a git repository{fmt.RESET}")
        sys.exit(1)

    for fp in files:
        print(fp)


def cmd_show_languages(args):
    from gitline.languages import EXT_MAP

    # Group by language
    by_lang = {}
    for ext, lang in sorted(EXT_MAP.items(), key=lambda x: x[1]):
        by_lang.setdefault(lang, []).append(ext)

    print(f"  {fmt.BOLD}Supported Languages ({len(by_lang)}){fmt.RESET}")
    print()
    for lang, exts in sorted(by_lang.items()):
        ext_str = ", ".join(exts)
        color = fmt.LANG_COLORS.get(lang, fmt.WHITE)
        print(f"  {color}{lang:<18}{fmt.RESET} {ext_str}")


def main():
    parser = argparse.ArgumentParser(
        description="gitline — count lines of code per language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gitline                         # Count current directory
  gitline /path/to/project        # Count specific path
  gitline --format json           # JSON output
  gitline --format csv            # CSV output
  gitline --verbose               # Show per-file breakdown
  gitline diff main HEAD          # Diff between branches
  gitline languages               # List supported languages
""",
    )

    sub = parser.add_subparsers(dest="command")

    # count (default)
    p_count = sub.add_parser("count", aliases=["c"], help="Count lines of code")
    p_count.add_argument("path", nargs="?", default=".", help="Path to analyze")
    p_count.add_argument("--format", "-f", choices=["human", "json", "csv"],
                         default="human", help="Output format")
    p_count.add_argument("--verbose", "-v", action="store_true",
                         help="Show per-file breakdown")
    p_count.set_defaults(func=cmd_count)

    # diff
    p_diff = sub.add_parser("diff", help="Show diff stat between refs")
    p_diff.add_argument("base", nargs="?", default="main", help="Base ref")
    p_diff.add_argument("head", nargs="?", default="HEAD", help="Head ref")
    p_diff.add_argument("path", nargs="?", default=".", help="Repo path")
    p_diff.set_defaults(func=cmd_diff)

    # list files
    p_ls = sub.add_parser("files", aliases=["ls"], help="List tracked files")
    p_ls.add_argument("path", nargs="?", default=".", help="Repo path")
    p_ls.set_defaults(func=cmd_list_files)

    # languages
    p_langs = sub.add_parser("languages", help="List supported languages")
    p_langs.set_defaults(func=cmd_show_languages)

    args = parser.parse_args()

    if not args.command:
        # Default: count
        args = parser.parse_args(["count"] + sys.argv[1:])
        if hasattr(args, 'func'):
            args.func(args)
        return

    args.func(args)


if __name__ == "__main__":
    main()
