#!/data/data/com.termux/files/usr/bin/bash

set -e

# ==================================================
# MODERN TERMUX HOME — FULL FINAL INSTALLER
# ==================================================

# ---------- COLORS ----------
C_CYAN="\033[1;36m"
C_GREEN="\033[1;32m"
C_YELLOW="\033[1;33m"
C_RED="\033[1;31m"
C_RESET="\033[0m"

info(){ echo -e "${C_CYAN}[i]${C_RESET} $1"; }
ok(){ echo -e "${C_GREEN}[✓]${C_RESET} $1"; }
warn(){ echo -e "${C_YELLOW}[!]${C_RESET} $1"; }
die(){ echo -e "${C_RED}[x]${C_RESET} $1"; exit 1; }

# ---------- ENV CHECK ----------
[[ "$PREFIX" == *"com.termux"* ]] || die "Run this inside Termux only"

# ---------- UPDATE ----------
info "Updating Termux..."
pkg update -y && pkg upgrade -y

# ---------- PACKAGES ----------
info "Installing required packages..."
pkg install -y git curl nano python

# ---------- STORAGE ----------
termux-setup-storage

# ---------- USER INPUT ----------
read -p "Enter name for terminal prompt [AMAN]: " USER_NAME
USER_NAME="${USER_NAME:-AMAN}"

DEFAULT_DIR="/storage/emulated/0/zzz/kkk"
read -p "Default working directory [$DEFAULT_DIR]: " HOME_DIR
HOME_DIR="${HOME_DIR:-$DEFAULT_DIR}"
mkdir -p "$HOME_DIR"

# ---------- TERMUX DIR ----------
mkdir -p ~/.termux

# ---------- THEME ----------
info "Applying Argonaut (modern balanced theme)..."
cat > ~/.termux/colors.properties <<'EOF'
background=#0e1019
foreground=#fffaf4
cursor=#fffaf4
color0=#232323
color1=#ff000f
color2=#8ce10b
color3=#ffb900
color4=#008df8
color5=#6d43a6
color6=#00d8eb
color7=#ffffff
color8=#444444
color9=#ff2740
color10=#abe15b
color11=#ffd242
color12=#0092ff
color13=#9a5feb
color14=#67fff0
color15=#ffffff
EOF

# ---------- TERMUX PROPERTIES ----------
info "Setting Termux properties..."
cat > ~/.termux/termux.properties <<'EOF'
terminal-transcript-rows=40000
terminal-cursor-style=underline
terminal-cursor-blink-rate=500
use-black-ui=true
bell-character=ignore
EOF

# ---------- BASHRC PATH ----------
BASHRC="/data/data/com.termux/files/usr/etc/bash.bashrc"
BACKUP_DIR="$HOME/backup"
mkdir -p "$BACKUP_DIR"

# ---------- BACKUP ----------
if [[ -f "$BASHRC" ]]; then
  cp "$BASHRC" "$BACKUP_DIR/bash.bashrc.$(date +%F-%H%M%S)"
  ok "Old bashrc backed up"
fi

# ---------- WRITE NEW BASHRC ----------
info "Writing modern bash.bashrc..."

cat > "$BASHRC" <<EOF
# ==================================================
# MODERN TERMUX HOME — FINAL STABLE
# ==================================================

# ---- Prevent double execution ----
[[ -n "\$TERMUX_HOME_LOADED" ]] && return
export TERMUX_HOME_LOADED=1

# ---- Identity ----
USER_NAME="$USER_NAME"
HOME_DIR="$HOME_DIR"

# ---- History ----
HISTCONTROL=ignoreboth
HISTSIZE=3000
HISTFILESIZE=6000
shopt -s histappend
shopt -s autocd

# ---- Aliases ----
alias ll='ls -lh --group-directories-first'
alias la='ls -alh --group-directories-first'
alias c='clear'
alias cls='clear'
alias ..='cd ..'
alias e='nano'
alias g='git'

# ---- Clear Screen ----
clear

# ---- HOME ART ----
echo -e "\\033[1;36m"
echo "╭────────────────────────────╮"
echo "│  ▸ HOME :: \$USER_NAME      │"
echo "│  ▸ focus > excuses         │"
echo "│  ▸ build something real    │"
echo "╰────────────────────────────╯"
echo -e "\\033[0m"


# ---- Prompt ----
PS1='\\[\\033[36m\\]┌─(\\
\\[\\033[97m\\]'\$USER_NAME'\\
\\[\\033[31m\\] 〄 \\
\\[\\033[93m\\]\\D{%H:%M}\\
\\[\\033[36m\\])-[\\
\\[\\033[96m\\]\\w\\
\\[\\033[36m\\]]\\
\\n└─>> \\[\\033[0m\\]'

# ---- Default Directory ----
[[ -d "\$HOME_DIR" ]] && cd "\$HOME_DIR"
EOF

ok "Modern home setup completed"

echo
echo -e "${C_GREEN}✔ DONE.${C_RESET} Restart Termux to see your new HOME."
echo