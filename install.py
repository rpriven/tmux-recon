#!/usr/bin/python3

import os
import subprocess
import shutil
from pathlib import Path
import platform
import sys
import datetime
import hashlib
import argparse

# Colors for output
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
ORANGE = "\033[1;38;5;208m"
PURPLE = "\033[1;35m"
BOLD = "\033[1m"
RESET = "\033[0m"

HOME = Path.home()
DOTFILES_DIR = Path.cwd() / "dotfiles"
SCRIPTS_DIR = HOME / ".scripts"

command_map = {
    "ripgrep": "rg",
    "silversearcher-ag": "ag",
    "fzf": "fzf",
    "zoxide": "zoxide",
    "btop": "btop",
    "tmux": "tmux",
    "python3-pip": "pip3",
}

if os.geteuid() == 0:
        print_color(f"[!] Do not run this script as root. Please run it as a regular user. [!]", RED)
        sys.exit(1)


# ---------------------- Helpers ----------------------


def print_color(msg, *styles, **kwargs):
    style_seq = "".join(styles)
    print(f"{style_seq}{msg}{RESET}", **kwargs)

def print_banner():
    if shutil.which("figlet") and shutil.which("lolcat"):
        os.system("figlet Tmux-Recon | lolcat")
    else:
        print_color(f"\n==== TMUX-RECON Installer ====\n", CYAN)

def is_installed(pkg):
    cmd = command_map.get(pkg, pkg)
    return shutil.which(cmd) is not None

def is_running_in_tmux():
    return os.environ.get("TMUX") is not None


# ---------------------- Install ----------------------


def run_cmd(cmd, check=True, env=None):
    if env is None:
        env = os.environ.copy()
    try:
        with subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env
        ) as process:
            for line in process.stdout:
                print(line, end="")
        if process.returncode != 0 and check:
            raise subprocess.CalledProcessError(process.returncode, cmd)
    except subprocess.CalledProcessError as e:
        print_color(f"[!] Command failed: {cmd}", RED)
        raise e

def install_all_required():
    all_required = [
        "wget", "tmux", "curl", "python3", "python3-pip", "xclip",
        "most", "fzf", "zoxide", "silversearcher-ag", "ripgrep", "gawk", "btop"
    ]
    install_packages(all_required)

def install_packages(package_list):
    print_color("\n=== Installing Packages ===\n", PURPLE)
    failed = []

    for prog in package_list:
        if is_installed(prog):
            print_color(f"[OK] {prog}", GREEN)
        else:
            print_color(f"[!] {prog} is not installed, installing...", YELLOW)
            try:
                run_cmd(f"sudo apt install -y {prog} -o=Dpkg::Use-Pty=0")
                print_color(f"[+] Installed {prog}", GREEN)
            except subprocess.CalledProcessError as e:
                print_color(f"[!] Failed to install {prog}", RED)
                failed.append(prog)
                continue

    if failed:
            print_color("\n[!] Some packages failed to install:", ORANGE)
            for p in failed:
                print_color(f" - {p}", RED)

def install_oh_my_tmux():
    print_color(f"\n[+] Installing Oh-my-tmux!...", CYAN)
    tmux_dir = HOME / ".tmux"
    if not tmux_dir.exists():
        try:
            run_cmd("git clone --single-branch https://github.com/gpakosz/.tmux.git ~/.tmux")
            run_cmd("ln -s -f ~/.tmux/.tmux.conf ~/.tmux.conf")
            run_cmd("cp ~/.tmux/.tmux.conf.local ~/.tmux.conf.local")
            print_color(f"[OK] Oh-my-tmux! installed", GREEN)
        except subprocess.CalledProcessError:
            print_color("Failed to install Oh-my-tmux!", RED)
    else:
        print_color(f"[i] Oh My Tmux! already installed. Skipping.", YELLOW)

def install_arsenal():
    arsenal_dir = HOME / "arsenal"
    if arsenal_dir.exists() and any(arsenal_dir.iterdir()):
        print_color("Arsenal already cloned", GREEN)
        return
    try:
        print_color("[+] Installing Arsenal...", CYAN)
        run_cmd(f"git clone https://github.com/Orange-Cyberdefense/arsenal.git {arsenal_dir}")
        run_cmd(f"python3 -m pip install -r {arsenal_dir}/requirements.txt")
        print_color("Arsenal installed. You can run it with './run' inside ~/arsenal", GREEN)
    except subprocess.CalledProcessError:
        print_color("Failed to install Arsenal", RED)


# ---------------------- Zsh ----------------------


def install_zsh():
    shell = os.environ.get("SHELL", "unknown")
    if "zsh" not in shell:
        print_color(f"\n[?] You are not using zsh. Would you like to install and use zsh? (y/n): ", ORANGE, end="")
        choice = input().strip().lower()
        if choice == "y":
            try:
                print_color("[+] Installing zsh...", CYAN)
                run_cmd("sudo apt install -y zsh -o=Dpkg::Use-Pty=0")
                real_user = os.getenv("SUDO_USER") or os.getenv("USER")
                run_cmd(f"sudo chsh -s $(which zsh) {real_user}")
                #run_cmd("sudo chsh -s $(which zsh)")
                print_color("\n=== Configuring Your Shell ===\n", PURPLE)
                print_color(f"[+] zsh installed and set as default. Please restart your shell.\n", GREEN)
            except subprocess.CalledProcessError:
                print_color("Failed to install zsh", RED)


def install_zsh_plugins():
    zsh_custom = HOME / ".zsh-custom"
    zsh_custom.mkdir(exist_ok=True)

    plugins = {
        "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions",
        "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting"
    }

    for name, repo in plugins.items():
        dest = zsh_custom / name
        if not dest.exists():
            print_color("[+] Installing zsh plugins...", CYAN)
            run_cmd(f"git clone {repo} {dest}")

    append_block(HOME / ".zshrc", "zsh-plugins", zsh_plugins_block)

zsh_plugins_block = f"""
source {HOME}/.zsh-custom/zsh-autosuggestions/zsh-autosuggestions.zsh
source {HOME}/.zsh-custom/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
""".strip()


# ---------------------- Dev ----------------------


def install_dev():
    print_color("\n=== Installing Developer Tools ===\n", PURPLE)
    dev_tools = ["git", "docker.io", "docker-compose", "cmake"]
    for prog in dev_tools:
        if shutil.which(prog) is None:
            print_color(f"[!] {prog} is not installed, installing...", YELLOW)
            try:
                # run_cmd(f"sudo apt install -y {prog}")
                run_cmd(f"sudo DEBIAN_FRONTEND=noninteractive apt install -y {prog} -o=Dpkg::Use-Pty=0")
                print_color(f"[+] Installed {prog}", GREEN)
            except subprocess.CalledProcessError:
                print_color(f"[!] Failed to install {prog}", RED)
        else:
            print_color(f"[OK] {prog}", GREEN)

    # --- Install Miniconda (simplified) ---
    miniconda_dir = HOME / "miniconda3"
    miniconda_sh = miniconda_dir / "miniconda.sh"
    conda_bin = miniconda_dir / "bin"
    os.environ["PATH"] += f":{conda_bin}"

    '''
    # Clean
    if args.clean:
        print_color("[!] Cleaning existing Miniconda install", YELLOW)
        shutil.rmtree(miniconda_dir, ignore_errors=True)
    # End clean
    '''

    if miniconda_dir.exists() or shutil.which("conda"):
        print(f"[✔] Miniconda already installed", GREEN)
        # new lines
        try:
            run_cmd("conda --version")
            print_color("[✔] Miniconda already installed", GREEN)
        except subprocess.CalledProcessError:
            print_color("[!] Conda found, but appears broken. Reinstalling...", YELLOW)
            shutil.rmtree(miniconda_dir, ignore_errors=True)
        # end new lines
    else:
        try:
            run_cmd(f"mkdir -p {miniconda_dir}")
            run_cmd(f"wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O {miniconda_sh}")
            run_cmd(f"bash {miniconda_sh} -b -u -p {miniconda_dir}")
            print_color(f"[+] Miniconda installed at {miniconda_dir}", GREEN)
            run_cmd(f"rm {miniconda_sh}")
        except subprocess.CalledProcessError:
            print_color("[!] Failed to install Miniconda", RED)

    # Add conda to shell startup
    conda_export_block = f"""
export PATH="$PATH:{conda_bin}"
""".strip()

    append_block(HOME / ".bashrc", "miniconda-path", conda_export_block)
    append_block(HOME / ".zshrc", "miniconda-path", conda_export_block)

    # Also for current runtime
    os.environ["PATH"] += f":{conda_bin}"

GO_INSTALLED = False  # Global flag so we don’t reinstall during same script run

def install_go():
    # Clean
    if args.clean:
        print_color("[!] Cleaning existing Go install", YELLOW)
        run_cmd("sudo rm -rf /usr/local/go")
        shutil.rmtree(HOME / "go", ignore_errors=True)
    # End clean

    go_bin = Path("/usr/local/go/bin/go")

    # Already installed?
    if shutil.which("go") or go_bin.exists():
        print_color("[✔] Golang already installed", GREEN)

        # Still need to return a valid environment!
        gopath = HOME / "go"
        gopath_bin = gopath / "bin"
        go_env = os.environ.copy()
        go_env["GOPATH"] = str(gopath)
        go_env["PATH"] += f":/usr/local/go/bin:{gopath_bin}"
        return go_env

    print_color("[+] Installing Golang...", CYAN)

    run_cmd("wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz")
    run_cmd("sudo rm -rf /usr/local/go")
    run_cmd("sudo tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz")

    # Set up environment
    gopath = HOME / "go"
    gopath_bin = gopath / "bin"
    go_export_block = f"""
export GOPATH="$HOME/go"
export PATH="$PATH:/usr/local/go/bin:$GOPATH/bin"
""".strip()

    append_block(HOME / ".bashrc", "golang-paths", go_export_block)
    append_block(HOME / ".zshrc", "golang-paths", go_export_block)

    # Local env for Python subprocess
    go_env = os.environ.copy()
    go_env["GOPATH"] = str(gopath)
    go_env["PATH"] += f":/usr/local/go/bin:{gopath_bin}"

    try:
        run_cmd("go version", env=go_env)
        print_color("[✔] Golang installed successfully", GREEN)
    except subprocess.CalledProcessError:
        print_color("[!] Golang installation failed to verify", RED)

    return go_env


# ---------------------- Dotfiles ----------------------


def append_block(rcfile, tag, block):
    if not rcfile.exists():
        rcfile.touch()
    backup_file(rcfile)

    content = rcfile.read_text()
    if block.strip() in content:
        print_color(f"[=] {rcfile.name} already includes block for {tag}", YELLOW)
    else:
        with rcfile.open("a") as f:
            f.write(f"\n# {tag}\n{block.strip()}\n")
        print_color(f"[+] Added {tag} block to {rcfile.name}", GREEN)

def install_dotfiles():
    print_color(f"[+] Installing dotfiles...", CYAN)

    bashrc = HOME / ".bashrc"
    zshrc = HOME / ".zshrc"

    bash_block = f"""
source {DOTFILES_DIR / 'bash.bash'}
source {DOTFILES_DIR / 'aliases.sh'}
export PATH="$HOME/arsenal:$HOME/.scripts:$PATH"
""".strip()

    zsh_block = f"""
source {DOTFILES_DIR / 'zsh.zsh'}
source {DOTFILES_DIR / 'aliases.sh'}
export PATH="$HOME/arsenal:$HOME/.scripts:$PATH"
""".strip()

    append_block(bashrc, "tmux-recon", bash_block)
    append_block(zshrc, "tmux-recon", zsh_block)

def hash_file(file_path):
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def backup_file(file):
    if file.exists():
        existing_hash = hash_file(file)
        # Check latest backup hash (if any)
        backup_files = sorted(file.parent.glob(file.name + ".bak-*"))
        latest_backup = backup_files[-1] if backup_files else None
        if latest_backup and hash_file(latest_backup) == existing_hash:
            print_color(f"[=] {file.name} unchanged, skipping backup", YELLOW)
            return
        # Make new backup
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = file.with_suffix(file.suffix + f".bak-{timestamp}")
        shutil.copy2(file, backup)
        print_color(f"[~] Backed up {file.name} to {backup.name}", YELLOW)


# ---------------------- Scripts & Plugins ----------------------


def setup_scripts_dir():
    print_color("\n=== Installing Scripts ===\n", PURPLE)
    print_color(f"[+] Setting up ~/.scripts directory and adding to PATH...", CYAN)
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
    print_color(f"[+] Installing tmux plugin manager (TPM)...", CYAN)
    tpm_dir = HOME / ".tmux/plugins/tpm"
    if not tpm_dir.exists():
        run_cmd("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")

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

def install_projectdiscovery():
    go_env = install_go()

    if shutil.which("pdtm") is None:
        print_color("\n=== Installing pdtm ===\n", PURPLE)
        print_color("[+] Installing PDTM (ProjectDiscovery Tool Manager)...", CYAN)

        go_env = install_go()  # still updates env with GOPATH, etc.
        run_cmd("go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest", env=go_env)
        print_color("[+] PDTM installed", GREEN)
    else:
        print_color("[✓] PDTM already installed", GREEN)

    # Confirm if user wants to install ALL tools now
    print_color("\n[?] Do you want to install *all* ProjectDiscovery tools now? (y/N): ", ORANGE, end="")
    choice = input().strip().lower()
    if choice == "y":
        run_cmd("$HOME/go/bin/pdtm -install-all || pdtm -install-all")
        print_color("[+] ProjectDiscovery tools installed", GREEN)
    else:
        print_color("[i] You can install tools later with:", CYAN)
        print_color("    pdtm -install-all", GREEN)

    # Display output, confirm it's running
    try:
        run_cmd("pdtm", env=go_env)
    except subprocess.CalledProcessError:
        print_color("[!] pdtm installed, but command failed to run", RED)


# ---------------------- Output ----------------------


def shell_reminder():
    shell = os.environ.get("SHELL", "")
    rc_file = "~/.bashrc"
    if "zsh" in shell:
        rc_file = "~/.zshrc"
    print_color(f"\n[i]", YELLOW, end=" "); print_color(f"To activate new PATH changes, run:", PURPLE, end=" ")
    print_color(f"source {rc_file}\n", GREEN)

def print_usage(dev=False, arsenal=False, pdtm=False):
    print_color(f"\n[✔] tmux-recon installation complete!", GREEN)

    print("\nNext steps:", ORANGE)

    # General
    print_color("1.", PURPLE, end=" ")
    print("Restart your terminal or run", end=" ")
    print_color("zsh -l", GREEN)

    print_color("2.", PURPLE, end=" ")
    print("Run tmux:", end=" ")
    print_color("tmux", GREEN)

    print_color("3.", PURPLE, end=" ")
    print("Press", end=" ")
    print_color("prefix + I", GREEN)
    print("   to install tmux plugins")

    print_color("4.", PURPLE, end=" ")
    print("Scripts available in ~/.scripts (already in your $PATH)")

    print_color("5.", PURPLE, end=" ")
    print("To install Oh My Zsh later, run:")
    print_color('   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"\n', GREEN)

    # print("    ", end="")
    print_color("[i]", PURPLE, end=" "); print("Oh-my-tmux! uses Powerline symbols.")
    print("    For best results, use a Nerd Font or install PowerlineSymbols.otf")
    print_color("    https://github.com/ryanoasis/nerd-fonts\n", CYAN)

    # Dev tools usage
    if dev:
        print_color("\n[Dev Tools]\n", PURPLE)
        print_color("[-] Miniconda usage", GREEN)
        print_color("→", CYAN, end=" "); print("To start conda:", end=" ")
        print("Run", end=" "); print_color("conda init", GREEN)
        print("Then restart terminal and use", end=" "); print_color("conda activate <env>\n", GREEN)

    # Arsenal
    if arsenal:
        print_color("\n[Arsenal Usage]\n", PURPLE)
        print_color("→", CYAN, end=" "); print("To run Arsenal:", end=" ")
        print_color("cd", GREEN, end=" "); print("into", end=" "); print_color("~/arsenal", GREEN, end=" "); print("and run:", end=" ")
        print_color("./run\n", GREEN)

    # ProjectDiscovery usage
    if pdtm:
        print_color("\n[ProjectDiscovery's Open Source Tool Manager (pdtm)]\n", PURPLE)
        print_color("[i]", CYAN, end=" "); print("Tools were not installed automatically.")
        print_color("→", CYAN, end=" "); print("To install tools manually:", end=" ")
        print_color("pdtm -ia", GREEN)
        print("You can install individual tools with:", end=" "); print_color("pdtm -i nuclei\n", GREEN)


# ---------------------- Argparse --------------------


def parse_args():
    parser = argparse.ArgumentParser(description="tmux-recon installer")
    parser.add_argument("--dev", action="store_true", help="Install Dev Tools")
    parser.add_argument("--pdtm", action="store_true", help="Install ProjectDiscovery Open Source Tool Manager")
    parser.add_argument("--arsenal", action="store_true", help="Install Arsenal")
    parser.add_argument("--all", action="store_true", help="Install Everything")
    parser.add_argument("--clean", action="store_true", help="Force reinstallation of all tools")
    return parser.parse_args()

args = parse_args()

if args.all:
    args.dev = args.arsenal = args.pdtm = True


# ---------------------- Main ----------------------


def main():
    if is_running_in_tmux():
        print_color(f"[!] It looks like you're running inside a tmux session. Consider exiting and re-running.", RED)

    print_banner()
    print_color(f"[!] Heads up: This might take a minute...", ORANGE)
    run_cmd("sudo -v")
    run_cmd("sudo apt update")

    installed = []

    install_all_required()
    install_oh_my_tmux()
    install_zsh()
    install_dotfiles()
    install_zsh_plugins()
    ensure_powerline_symbols()
    setup_scripts_dir()
    install_tmux_plugins()

    if args.dev:
        install_go()
        install_dev()
        installed.append("Dev Tools")

    if args.arsenal:
        install_arsenal()
        installed.append("Arsenal")

    if args.pdtm:
        install_go()
        install_projectdiscovery()
        installed.append("ProjectDiscovery's Open Source Tool Manager")

    print_color("\n=== Finalizing... ===\n", PURPLE)
    print_color("\n[✔] Installation summary:", GREEN)
    if installed:
        print_color(f"Installed: {', '.join(installed)}", CYAN)
    else:
        print_color("Nothing extra installed.", YELLOW)
    
    print_usage(dev=args.dev, arsenal=args.arsenal, pdtm=args.pdtm)
    shell_reminder()

if __name__ == "__main__":
    main()
