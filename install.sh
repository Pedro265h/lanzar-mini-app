#!/usr/bin/env bash
# install.sh — Instala el skill "lanzar-mini-app" en Claude Code (Mac / Linux)
#
# Uso (curl 1-liner):
#   curl -fsSL https://raw.githubusercontent.com/Pedro265h/lanzar-mini-app/main/install.sh | bash
#
# O clonando manualmente:
#   git clone https://github.com/Pedro265h/lanzar-mini-app.git
#   bash lanzar-mini-app/install.sh

set -euo pipefail

SKILL_NAME="lanzar-mini-app"
REPO_URL="https://github.com/Pedro265h/lanzar-mini-app.git"
TARGET="$HOME/.claude/skills/$SKILL_NAME"

echo ""
echo "  ┌─────────────────────────────────────────────────┐"
echo "  │  Instalador: skill 'lanzar-mini-app'            │"
echo "  │  Para Claude Code — Pedro Hernández             │"
echo "  └─────────────────────────────────────────────────┘"
echo ""

# Detectar OS
case "$(uname -s)" in
  Darwin*) OS_NAME="macOS" ;;
  Linux*)  OS_NAME="Linux" ;;
  *)       OS_NAME="Desconocido" ;;
esac
echo "  ✓ Sistema operativo detectado: $OS_NAME"

# Verificar requisitos
if ! command -v git >/dev/null 2>&1; then
  echo ""
  echo "  ✗ ERROR: necesitas Git instalado."
  echo "    En Mac: instala desde https://git-scm.com o ejecuta 'xcode-select --install'"
  echo "    En Linux: 'sudo apt install git' o equivalente"
  exit 1
fi
echo "  ✓ Git OK"

# Verificar que ~/.claude existe (Claude Code instalado)
if [ ! -d "$HOME/.claude" ]; then
  echo ""
  echo "  ✗ ERROR: no encuentro la carpeta ~/.claude"
  echo "    ¿Tienes Claude Code instalado?"
  echo "    Instala primero desde: https://claude.com/code"
  exit 1
fi
echo "  ✓ Claude Code detectado"

# Crear carpeta de skills si no existe
mkdir -p "$HOME/.claude/skills"

# Si ya existe la skill, preguntar
if [ -d "$TARGET" ]; then
  echo ""
  echo "  ⚠️  Ya tienes 'lanzar-mini-app' instalado en $TARGET"
  if [ -t 0 ]; then
    read -p "  ¿Quieres actualizarlo a la última versión? (s/n): " RESP
  elif [ -e /dev/tty ]; then
    read -p "  ¿Quieres actualizarlo a la última versión? (s/n): " RESP < /dev/tty
  else
    RESP="n"
  fi
  if [[ ! "$RESP" =~ ^[Ss]$ ]]; then
    echo "  Instalación cancelada. Tu skill actual queda intacta."
    exit 0
  fi
  echo "  Removiendo versión anterior..."
  rm -rf "$TARGET"
fi

# Clonar el repo (sin .git para que sea más limpio)
echo ""
echo "  → Descargando skill desde GitHub..."
TMP_DIR=$(mktemp -d)
git clone --depth 1 --quiet "$REPO_URL" "$TMP_DIR/lanzar-mini-app"
rm -rf "$TMP_DIR/lanzar-mini-app/.git"
mv "$TMP_DIR/lanzar-mini-app" "$TARGET"
rm -rf "$TMP_DIR"

echo "  ✓ Skill instalado en: $TARGET"

# Mensaje final
echo ""
echo "  ┌─────────────────────────────────────────────────┐"
echo "  │  🎉 INSTALACIÓN COMPLETA                        │"
echo "  └─────────────────────────────────────────────────┘"
echo ""
echo "  Para usar el skill:"
echo ""
echo "    1. Abre (o reinicia) Claude Code"
echo "    2. Escribe: '/lanzar-mini-app'  o  'quiero lanzar una mini app'"
echo "    3. Claude te guía fase por fase, de la idea a la campaña"
echo ""
echo "  Necesitas cuentas de Cloudflare, Hotmart y Meta."
echo "  Los requisitos completos están en el README."
echo ""
echo "  Creada por Pedro"
echo ""
echo "  ¿Quieres aprender a crear y lanzar tus propias apps"
echo "  con IA? Suscríbete a la comunidad:"
echo "    👥 https://www.skool.com/pedro-hernandez-7383"
echo ""
