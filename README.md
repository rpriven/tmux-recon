# 🛠️ install.py – Modular Installer for Dev, Sec, and Recon Tools

This is a Python-based modular installer script designed to quickly set up useful packages, dotfiles, zsh, oh-my-tmux, dev environment, recon tools and more with minimal hassle. Whether you're spinning up a fresh VM, container, or workstation, `install.py` handles all the heavy lifting.

---

## 📦 Features

- 🔧 **Developer Tools**: Installs Docker, Git, Miniconda, and more
- 🔍 **Recon Arsenal**: Pulls top-tier open-source recon tools
- 🕵️‍♂️ **ProjectDiscovery Support**: Installs `pdtm` and optionally all supported tools
- 📦 **Golang Installer**: Smart Go install with PATH updates
- 🧼 **Cleanup Options**: Use `--clean` to wipe broken installs
- 🧠 **Intelligent**: Skips installs if already present, checks integrity
- 🐚 **Shell Updates**: Injects env changes into `.bashrc`/`.zshrc`

---

## 🚀 Usage

Clone this repo and run:

```bash
python3 install.py [OPTIONS]
```

### Available Flags:

| Flag         | Status  | Description                                                |
|--------------|---------|------------------------------------------------------------|
| `--all`      |    ✅   | Installs everything (Dev + Arsenal + ProjectDiscovery)     |
| `--dev`      |    ✅   | Installs developer tooling (docker, git, miniconda, etc.)  |
| `--arsenal`  |    ✅   | Installs recon tools and common utilities                  |
| `--pdtm`     |    ✅   | Installs ProjectDiscovery tools                            |
| `--clean`    |         | Removes broken or partial installations (e.g., conda)      |
| `--dry-run`  |         | Prints planned actions but makes no changes                |

---

## 🧠 Notes

- Make sure to **`source ~/.bashrc` or `~/.zshrc`** after running to apply path/env updates.
- If you skip full ProjectDiscovery install, you can always run later:

```bash
pdtm -install-all
```

- Tools are installed under your home directory when possible.
- Requires `sudo` for some packages (e.g., docker, go).

---

## 🧪 Tested On

- ✅ Ubuntu 20.04 / 22.04
- ✅ Debian-based containers
- 🐳 Compatible with Docker and ephemeral environments

---

## 🧰 Tools Included (Sample)

### Developer Tools:
- `git`
- `docker.io`
- `docker-compose`
- `miniconda` (conda CLI)

### ProjectDiscovery:
- `pdtm` (tool manager)
- All tools available via: `pdtm -install-all`
- `httpx`
- `subfinder`
- `nuclei`

---

## 🧼 Cleanup

If something goes wrong or you want to start fresh:

```bash
python3 install.py --clean
```

---

## 🙏 Contributions Welcome

Contributions are **greatly** appreciated!

Feel free to open a PR if you want to add new tools, distros, or enhancements!

---

## 📄 License

MIT License
