#!/usr/bin/env bash
# =====================================================================
#  LA RATA - instalador para Linux (Debian/Ubuntu y derivados)
#  Deja la herramienta lista para usar con:  larata start | stop
#  y como acceso directo en el menu de aplicaciones (con icono).
#
#  Uso:
#    ./install.sh            instala para el usuario actual
#    sudo ./install.sh       instala a nivel sistema (/opt + /usr/local/bin)
#  Autor: Miguel (ElSuinda).
# =====================================================================
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$(id -u)" -eq 0 ]; then
  PREFIX_APP="/opt/larata"; BIN="/usr/local/bin/larata"
  ICON_DIR="/usr/share/icons/hicolor/256x256/apps"; DESKTOP_DIR="/usr/share/applications"
else
  PREFIX_APP="$HOME/.local/share/larata"; BIN="$HOME/.local/bin/larata"
  ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"; DESKTOP_DIR="$HOME/.local/share/applications"
fi

echo "[*] Instalando LA RATA en $PREFIX_APP"
mkdir -p "$PREFIX_APP" "$(dirname "$BIN")" "$ICON_DIR" "$DESKTOP_DIR"

# copiar la app (codigo + recursos)
cp -f "$SRC/app.py" "$SRC/larata" "$PREFIX_APP/"
cp -rf "$SRC/core" "$SRC/templates" "$SRC/static" "$PREFIX_APP/"
cp -rf "$SRC/assets" "$PREFIX_APP/" 2>/dev/null || true
chmod +x "$PREFIX_APP/larata"

# entorno virtual propio con dependencias
echo "[*] Creando entorno virtual e instalando dependencias..."
python3 -m venv "$PREFIX_APP/.venv"
"$PREFIX_APP/.venv/bin/pip" install --quiet --upgrade pip
"$PREFIX_APP/.venv/bin/pip" install --quiet -r "$SRC/requirements.txt"

# comando global
ln -sf "$PREFIX_APP/larata" "$BIN"

# icono + acceso directo
[ -f "$SRC/assets/icono-256.png" ] && cp -f "$SRC/assets/icono-256.png" "$ICON_DIR/larata.png"
cp -f "$SRC/larata.desktop" "$DESKTOP_DIR/larata.desktop"
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q "$(dirname "$(dirname "$(dirname "$ICON_DIR")")")" 2>/dev/null || true

echo ""
echo "[+] LA RATA instalada."
echo "    - Comando:        larata start | stop | status"
echo "    - Acceso directo: menu de aplicaciones -> LA RATA"
echo "    - App en:         $PREFIX_APP"
if [ "$(id -u)" -ne 0 ]; then
  case ":$PATH:" in *":$HOME/.local/bin:"*) : ;; *) echo "    (!) Agrega ~/.local/bin al PATH para usar 'larata' directamente.";; esac
fi
echo ""
echo "    Gracias por usar mi soft! - El Suinda @v@"
