#!/data/data/com.termux/files/usr/bin/env python3

import os
import shutil
import sys

# ====== COLOR THEMES ======
THEMES = {
    1: ("Ubuntu", """background=#300a24
foreground=#ffffff
cursor=#ffffff
color0=#2E3436
color1=#CC0000
color2=#4E9A06
color3=#C4A000
color4=#3465A4
color5=#75507B
color6=#06989A
color7=#D3D7CF
color8=#555753
color9=#EF2929
color10=#8AE234
color11=#FCE94F
color12=#729FCF
color13=#AD7FA8
color14=#34E2E2
color15=#EEEEEC
"""),
    2: ("Argonaut", """background=#0e1019
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
"""),
    3: ("Material", """background:#263238
foreground:#eceff1
color0:#263238
color8:#37474f
color1:#ff9800
color9:#ffa74d
color2:#8bc34a
color10:#9ccc65
color3:#ffc107
color11:#ffa000
color4:#03a9f4
color12:#81d4fa
color5:#e91e63
color13:#ad1457
color6:#009688
color14:#26a69a
color7:#cfd8dc
color15:#eceff1
"""),
    4: ("Dracula", """foreground=#f8f8f2
cursor=#f8f8f2
background=#282a36
color0=#000000
color8=#4d4d4d
color1=#ff5555
color9=#ff6e67
color2=#50fa7b
color10=#5af78e
color3=#f1fa8c
color11=#f4f99d
color4=#bd93f9
color12=#caa9fa
color5=#ff79c6
color13=#ff92d0
color6=#8be9fd
color14=#9aedfe
color7=#bfbfbf
color15=#e6e6e6
"""),
    5: ("Nancy", """foreground:     #fff
background:     #010101
cursor:    #e5e5e5
color0:         #1b1d1e
color1:         #f92672
color2:         #82b414
color3:         #fd971f
color4:         #4e82aa
color5:         #8c54fe
color6:         #465457
color7:         #ccccc6
color8:         #505354
color9:         #ff5995
color10:        #b6e354
color11:        #feed6c
color12:        #0c73c2
color13:        #9e6ffe
color14:        #899ca1
color15:        #f8f8f2
"""),
    6: ("Isotope", """foreground:   #d0d0d0
background:   #000000
cursor:  #d0d0d0
color0:       #000000
color1:       #ff0000
color2:       #33ff00
color3:       #ff0099
color4:       #0066ff
color5:       #cc00ff
color6:       #00ffff
color7:       #d0d0d0
color8:       #808080
color9:       #ff0000
color10:      #33ff00
color11:      #ff0099
color12:      #0066ff
color13:      #cc00ff
color14:      #00ffff
color15:      #ffffff
"""),
}

# ====== ASCII ART BANNER ======
BANNER = r"""
\033[1;36m
████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝ 
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗ 
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝
\033[0m
"""

# ====== COLORED PRINT HELPERS ======
def info(msg): print(f"\033[1;34m[i]\033[0m {msg}")
def warn(msg): print(f"\033[1;33m[!]\033[0m {msg}")
def error(msg): print(f"\033[1;31m[x]\033[0m {msg}")
def ok(msg): print(f"\033[1;32m[✓]\033[0m {msg}")

# ====== TERMUX VISUALS ======
def set_theme(theme_num):
    theme_name, theme_content = THEMES[theme_num]
    colors_path = os.path.expanduser("~/.termux/colors.properties")
    os.makedirs(os.path.dirname(colors_path), exist_ok=True)
    with open(colors_path, "w") as f:
        f.write(theme_content)
    ok(f"Theme '{theme_name}' applied.")

def set_termux_properties():
    prop_path = os.path.expanduser("~/.termux/termux.properties")
    os.makedirs(os.path.dirname(prop_path), exist_ok=True)
    props = {
        "terminal-transcript-rows": "40000",
        "terminal-cursor-blink-rate": "500",
        "terminal-cursor-style": "underline",
        "use-black-ui": "true",
        "bell-character": "ignore"
    }
    lines = []
    if os.path.exists(prop_path):
        with open(prop_path, "r") as f:
            lines = f.readlines()
    # Remove old settings
    lines = [l for l in lines if not any(l.strip().startswith(k) for k in props)]
    # Add new settings
    lines += [f"{k} = {v}\n" for k, v in props.items()]
    with open(prop_path, "w") as f:
        f.writelines(lines)
    ok("Termux properties set.")

def backup_and_write_bashrc(username, default_cd):
    etc = "/data/data/com.termux/files/usr/etc"
    bashrc_path = os.path.join(etc, "bash.bashrc")
    backup_path = os.path.join(os.path.expanduser("~/backup/"), "old_bash.bashrc")
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    if os.path.exists(bashrc_path):
        shutil.copy(bashrc_path, backup_path)
        ok(f"Backed up old bashrc to {backup_path}")
    # Write new bashrc with ASCII art and prompt
    bashrc = f"""\
#######################################
#                                     #
# Termux bash.bashrc                  #
# Modified by: Python Visuals Script  #
#                                     #
#######################################

user_name="{username}"
editor="nano"
export GREP_COLOR="1;32"
export MANPAGER="less -R --use-color -Dd+g -Du+b"
export EDITOR=$editor
export SUDO_EDITOR=$editor
export VISUAL="vim"
export USER=$user_name
export ETC="/data/data/com.termux/files/usr/etc"
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000
shopt -s histappend
shopt -s histverify
shopt -s extglob
shopt -s autocd
bind 'TAB:menu-complete'
sym="〄"
bar_cr="34"
name_cr="37"
end_cr="37"
dir_cr="36"
PS1='\\[\\033[0;${{bar_cr}}m\\]┌──(\\[\\033[1;${{name_cr}}m\\]${{user_name}}\\[\\e[31m\\]${{sym}}\\[\\e[0m\\]\\[\\e[93m\\]\\D{{%H:%M:%S}}\\[\\e[0m\\]\\[\\033[0;${{bar_cr}}m\\])-[\\[\\033[0;${{dir_cr}}m\\]\\w\\[\\033[0;${{bar_cr}}m\\]]\\n\\[\\033[0;${{bar_cr}}m\\]└─\\[\\033[1;${{end_cr}}m\\]>>\\[\\033[0m\\] '
alias ..='cd ..'
alias ll='ls -lFh'
alias la='ls -alFh --group-directories-first'
alias c='clear'
alias e=$editor
{default_cd}
echo -e "\\e[0;37m"
clear
echo '████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗'
echo '╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝'
echo '   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝ '
echo '   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗ '
echo '   ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗'
echo '   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝'
echo
echo
echo
"""
    with open(bashrc_path, "w") as f:
        f.write(bashrc)
    ok("New bashrc with visuals and cd command applied.")

# ====== MAIN SETUP SCRIPT ======
def main():
    print(BANNER)
    # Theme selection
    print("\033[1;37mAvailable themes:\033[0m")
    for i, (name, _) in THEMES.items():
        print(f"  {i}. {name}")
    while True:
        try:
            theme_num = int(input("\033[1;36mChoose a theme (1-6): \033[0m"))
            if theme_num in THEMES:
                break
            else:
                warn("Invalid theme number.")
        except Exception:
            warn("Please enter a number.")
    # Username
    username = input("\033[1;36mEnter your name for prompt: \033[0m").strip() or "user"
    # Default directory
    default_directory = "/storage/emulated/0/zzz/kkk"
    target_directory = input(f"\033[1;36mEnter your default home directory (press Enter for {default_directory}): \033[0m").strip()
    if not target_directory:
        target_directory = default_directory
    os.system("termux-setup-storage")
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        ok(f"Created directory: {target_directory}")
    else:
        ok(f"Directory exists: {target_directory}")
    cd_command = f"cd {target_directory}\n"
    # Write to ~/.bashrc if not present
    bashrc_user = os.path.expanduser("~/.bashrc")
    if not os.path.exists(bashrc_user) or cd_command not in open(bashrc_user).read():
        with open(bashrc_user, "a") as f:
            f.write(cd_command)
        ok("Startup cd command added to ~/.bashrc.")
    else:
        info("cd command already present in ~/.bashrc.")
    # Theme, properties, bashrc
    set_theme(theme_num)
    set_termux_properties()
    backup_and_write_bashrc(username, cd_command)
    print("\n\033[1;32mSetup complete! Restart Termux to see your new look.\033[0m\n")

if __name__ == "__main__":
    main()
