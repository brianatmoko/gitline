#!/usr/bin/env bash
set -euo pipefail

BIN_DIR="$HOME/.local/bin"
LIB_DIR="$HOME/.local/lib/gitline"

mkdir -p "$BIN_DIR" "$LIB_DIR"

cp -r gitline "$LIB_DIR/"

cat > "$BIN_DIR/gitline" << 'SCRIPT'
#!/usr/bin/env bash
exec python3 -m gitline "$@"
SCRIPT

chmod +x "$BIN_DIR/gitline"

echo "gitline v2 terinstal!"
echo "  Jalankan: gitline"
echo "  Pastikan $BIN_DIR ada di PATH"
