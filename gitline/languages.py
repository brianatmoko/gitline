EXT_MAP = {
    # Assembly
    ".asm": "Assembly", ".s": "Assembly", ".S": "Assembly",
    # C
    ".c": "C", ".h": "C",
    # C++
    ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".hpp": "C++",
    ".hh": "C++", ".hxx": "C++", ".c++": "C++", ".h++": "C++",
    # C#
    ".cs": "C#",
    # Clojure
    ".clj": "Clojure", ".cljs": "Clojure", ".cljc": "Clojure",
    # CMake
    ".cmake": "CMake", "CMakeLists.txt": "CMake",
    # CoffeeScript
    ".coffee": "CoffeeScript",
    # CSS
    ".css": "CSS", ".scss": "SCSS", ".sass": "Sass", ".less": "Less",
    # Dart
    ".dart": "Dart",
    # Docker
    "Dockerfile": "Dockerfile",
    # Elixir
    ".ex": "Elixir", ".exs": "Elixir",
    # Erlang
    ".erl": "Erlang", ".hrl": "Erlang",
    # F#
    ".fs": "F#", ".fsx": "F#",
    # Go
    ".go": "Go",
    # Groovy
    ".groovy": "Groovy", ".gvy": "Groovy",
    # Haskell
    ".hs": "Haskell", ".lhs": "Haskell",
    # HTML
    ".html": "HTML", ".htm": "HTML", ".xhtml": "HTML",
    # Java
    ".java": "Java",
    # JavaScript / TypeScript
    ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    # JSON / YAML / TOML
    ".json": "JSON", ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML",
    # Julia
    ".jl": "Julia",
    # Jupyter
    ".ipynb": "Jupyter Notebook",
    # Kotlin
    ".kt": "Kotlin", ".kts": "Kotlin",
    # LaTeX
    ".tex": "LaTeX", ".sty": "LaTeX", ".cls": "LaTeX",
    # Lisp
    ".lisp": "Lisp", ".lsp": "Lisp", ".cl": "Lisp",
    # Lua
    ".lua": "Lua",
    # Make
    "Makefile": "Make", "makefile": "Make", "GNUmakefile": "Make",
    # Markdown
    ".md": "Markdown", ".markdown": "Markdown",
    # Nim
    ".nim": "Nim",
    # Nix
    ".nix": "Nix",
    # Objective-C
    ".m": "Objective-C", ".mm": "Objective-C",
    # OCaml
    ".ml": "OCaml", ".mli": "OCaml",
    # Pascal
    ".pas": "Pascal", ".pp": "Pascal",
    # Perl
    ".pl": "Perl", ".pm": "Perl", ".t": "Perl",
    # PHP
    ".php": "PHP", ".phtml": "PHP",
    # PowerShell
    ".ps1": "PowerShell", ".psm1": "PowerShell",
    # Protocol Buffers
    ".proto": "Protocol Buffers",
    # Python
    ".py": "Python", ".pyi": "Python", ".pyw": "Python",
    # R
    ".r": "R", ".R": "R",
    # Ruby
    ".rb": "Ruby", ".erb": "Ruby",
    # Rust
    ".rs": "Rust",
    # Scala
    ".scala": "Scala", ".sc": "Scala",
    # Shell
    ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell",
    ".fish": "Shell",
    # SQL
    ".sql": "SQL",
    # Swift
    ".swift": "Swift",
    # Tcl
    ".tcl": "Tcl",
    # Terraform
    ".tf": "Terraform", ".tfvars": "Terraform",
    # TeX
    ".sty": "TeX", ".cls": "TeX", ".bst": "TeX",
    # Verilog / VHDL
    ".v": "Verilog", ".vh": "Verilog", ".vhd": "VHDL", ".vhdl": "VHDL",
    # Vue
    ".vue": "Vue",
    # XML
    ".xml": "XML", ".xsd": "XML", ".xsl": "XML", ".svg": "XML",
    # Zig
    ".zig": "Zig",
}

SHEBANG_MAP = [
    (b"python", "Python"),
    (b"ruby", "Ruby"),
    (b"perl", "Perl"),
    (b"lua", "Lua"),
    (b"node", "JavaScript"),
    (b"deno", "JavaScript"),
    (b"bash", "Shell"),
    (b"sh", "Shell"),
    (b"zsh", "Shell"),
    (b"fish", "Shell"),
    (b"awk", "Shell"),
    (b"tclsh", "Tcl"),
    (b"racket", "Racket"),
    (b"racket", "Racket"),
    (b"guile", "Scheme"),
    (b"swipl", "Prolog"),
    (b"ghc", "Haskell"),
    (b"runghc", "Haskell"),
    (b"ocaml", "OCaml"),
    (b"sbcl", "Common Lisp"),
    (b"clisp", "Common Lisp"),
    (b"coffee", "CoffeeScript"),
    (b"crystal", "Crystal"),
    (b"dart", "Dart"),
    (b"elixir", "Elixir"),
    (b"escript", "Elixir"),
]


def detect_language(filepath, ext=None):
    ext = ext or ""
    ext_lower = ext.lower()

    # Check filename-based matches
    basename = filepath.rsplit("/", 1)[-1]
    if basename in EXT_MAP:
        return EXT_MAP[basename]

    # Check extension
    if ext_lower in EXT_MAP:
        return EXT_MAP[ext_lower]

    return None


def detect_shebang(first_bytes):
    for pattern, lang in SHEBANG_MAP:
        if pattern in first_bytes:
            return lang
    return None


def is_binary(filepath):
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" in chunk
    except Exception:
        return True  # Assume binary on error
