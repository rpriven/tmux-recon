#!/usr/bin/python3

import os
import subprocess
import shutil
from pathlib import Path
import platform
import sys

# Colors for output
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
RESET = "\033[0m"

HOME = Path.home()
DOTFILES_DIR = Path.cwd() / "dotfiles"
SCRIPTS_DIR = HOME / ".scripts"

# ---------------------- Helpers ----------------------
def print_color(msg, color):
    print(f"{color}{msg}{RESET}")

def run_cmd(cmd, check=True):
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError:
        print_color(f"[!] Command failed: {cmd}", RED)
        if check:
            sys.exit(1)

def backup_file(path):
    if path.exists():
        backup = path.with_suffix(path.suffix + ".bak")
        shutil.move(str(path), str(backup))
        print_color(f"[~] Backed up {path} -> {backup}", YELLOW)

def is_running_in_tmux():
    return os.environ.get("TMUX") is not None

# ---------------------- Steps ----------------------
def check_prereqs():
    print_color("[+] Checking prerequisites...", CYAN)
    required = ["wget", "tmux", "curl", "python3", "pip3", "xclip"]
    for prog in required:
        if shutil.which(prog) is None:
            print_color(f"[!] {prog} is not installed! Installing...", RED)
            run_cmd(f"sudo apt install -y {prog}")
            print_color(f"[+] Installed {prog}", GREEN)
        else:
            print_color(f"[OK] {prog}", GREEN)

def install_recommended():
    print_color("[+] Installing recommended tools...", CYAN)
    recommended = ["most", "fzf", "zoxide", "silversearcher-ag", "ripgrep", "gawk", "btop"]
    for prog in recommended:
        if shutil.which(prog) is None:
            print_color(f"[!] {prog} is not installed! Installing...", RED)
            run_cmd(f"sudo apt install -y {prog}")
            print_color(f"[+] Installed {prog}", GREEN)
        else:
            print_color(f"[OK] {prog}", GREEN)

def install_dev():
    print_color("[+] Installing developer tools...", CYAN)
    dev_tools = ["git", "docker.io", "docker-compose", "cmake"]
    for prog in dev_tools:
        if shutil.which(prog) is None:
            run_cmd(f"sudo apt install -y {prog}")
            print_color(f"[+] Installed {prog}", GREEN)
        else:
            print_color(f"[OK] {prog}", GREEN)

    # Install Golang
    if shutil.which("go") is None:
        print_color("[+] Installing Golang...", CYAN)
        run_cmd("wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz")
        run_cmd("sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz")
        os.environ["PATH"] += ":/usr/local/go/bin"
        print_color("[+] Golang installed", GREEN)

    # Install Miniconda (simplified)
    run_cmd("wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh")
    run_cmd("bash miniconda.sh -b -p $HOME/miniconda")
    print_color("[+] Miniconda installed at ~/miniconda", GREEN)


def install_dotfiles():
    print_color("[+] Installing dotfiles...", CYAN)

    # zsh
    zshrc = HOME / ".zshrc"
    backup_file(zshrc)
    if (DOTFILES_DIR / "zsh.zsh").exists():
        with zshrc.open("a") as f:
            f.write(f"\n# tmux-recon\nsource {DOTFILES_DIR / 'zsh.zsh'}\n")

    # bash
    bashrc = HOME / ".bashrc"
    backup_file(bashrc)
    if (DOTFILES_DIR / "bash.bash").exists():
        with bashrc.open("a") as f:
            f.write(f"\n# tmux-recon\nsource {DOTFILES_DIR / 'bash.bash'}\n")

    # aliases
    aliases = DOTFILES_DIR / "aliases.sh"
    if aliases.exists():
        for shell_file in [HOME / ".zshrc", HOME / ".bashrc"]:
            with shell_file.open("a") as f:
                f.write(f"source {aliases}\n")

    # Append tmux local settings (Oh My Tmux customizations)
    tmux_local = HOME / ".tmux.conf.local"
    if (DOTFILES_DIR / "tmux.tmux").exists():
        with tmux_local.open("a") as f:
            f.write("\n# tmux-recon customizations\n")
            f.write((DOTFILES_DIR / "tmux.tmux").read_text())

def ensure_powerline_symbols():
    conf_path = HOME / ".tmux.conf.local"
    powerline_lines = [
        'tmux_conf_theme_left_separator_main=""',
        'tmux_conf_theme_left_separator_sub=""',
        'tmux_conf_theme_right_separator_main=""',
        'tmux_conf_theme_right_separator_sub=""'
    ]
    with conf_path.open("r+") as f:
        content = f.read()
        if not any("tmux_conf_theme_left_separator_main" in line for line in content.splitlines()):
            f.write("\n# Powerline symbol customization\n")
            for line in powerline_lines:
                f.write(line + "\n")


def setup_scripts_dir():
    print_color("[+] Setting up ~/.scripts directory and adding to PATH...", CYAN)
    SCRIPTS_DIR.mkdir(exist_ok=True)
    shell_files = [HOME / ".zshrc", HOME / ".bashrc"]
    for file in shell_files:
        if file.exists():
            with file.open("r") as f:
                contents = f.read()
            if f"export PATH=\"$HOME/.scripts:$PATH\"" not in contents:
                with file.open("a") as f:
                    f.write("\n# Add tmux-recon scripts\nexport PATH=\"$HOME/.scripts:$PATH\"\n")

    for script in Path.cwd().glob("scripts/*"):
        if script.is_file():
            shutil.copy(script, SCRIPTS_DIR)
            print_color(f"[+] Installed script: {script.name}", GREEN)

def install_tmux_plugins():
    print_color("[+] Installing tmux plugin manager (TPM)...", CYAN)
    tpm_dir = HOME / ".tmux/plugins/tpm"
    if not tpm_dir.exists():
        run_cmd("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")

def print_usage(dev=False, pd=False):
    print_color("\n[✔] tmux-recon installation complete!", GREEN)
    print_color("""
Next steps:
1. Restart your terminal.
2. Open tmux: `tmux`
3. Press prefix + I to install plugins.
4. Scripts available in ~/.scripts (already in your $PATH).
5. To install Oh My Zsh later, run:
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
[i] Oh My Tmux! uses Powerline symbols.
    For best results, use a Nerd Font or install PowerlineSymbols.otf.
    https://github.com/ryanoasis/nerd-fonts
""", BOLD)
    if dev:
        print_color("[!] Developer tools installed.", CYAN)
    if pd:
        print_color("[!] ProjectDiscovery pdtm installed.", CYAN)
    else:
        print_color("[!] ProjectDiscovery NOT installed. Use --pd to include it.", YELLOW)

def install_projectdiscovery():
    print_color("[+] Installing ProjectDiscovery PDTM...", CYAN)
    run_cmd("go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest")

# ---------------------- Main ----------------------
def main():
    if is_running_in_tmux():
        print_color("[!] It looks like you're running inside a tmux session. Consider exiting and re-running.", RED)

    print_color("\n==== tmux-recon Installer ====\n", CYAN)

    args = sys.argv[1:]
    dev = "--dev" in args
    pd = "--pd" in args

    check_prereqs()
    install_recommended()
    install_oh_my_tmux()
    if dev:
        install_dev()
    shell = os.environ.get("SHELL", "unknown")
    if "zsh" not in shell:
        print_color("[?] You are not using zsh. Would you like to install and use zsh? (y/n): ", YELLOW)
        choice = input().strip().lower()
        if choice == "y":
            run_cmd("sudo apt install -y zsh")
            run_cmd("chsh -s $(which zsh)")
            print_color("[+] zsh installed and set as default. Please restart your shell.", GREEN)
    install_dotfiles()
    ensure_powerline_symbols()
    setup_scripts_dir()
    install_tmux_plugins()
    if pd:
        install_projectdiscovery()
    print_usage(dev=dev, pd=pd)

if __name__ == "__main__":
    main()
    