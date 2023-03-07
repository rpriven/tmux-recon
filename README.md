# tmux-recon

I put this here mostly so I can quickly setup my terminal and kali machine with my tmux and ohmytmux config as well as to run my tmux recon scripts.  I hope someone else finds this useful.

## Installation

I will eventually have a script to set all this up, but it is pretty simple:

1. Install Oh my tmux! at https://github.com/gpakosz/.tmux
2. Clone this repository
3. Modify .tmux.conf and .tmux.conf.local or use my versions
4. Add the bash aliases for recon and discovery automation

## Usage

### Recon

This runs several different nmap scans and enum4linux-ng

```bash
recon <ip>
```

### Discover

This runs nuclei, feroxbuster, katana and arjun

```bash
discover <ip>
```

This will be updated as there are quite a few improvements I hope to make that I'm currently testing.
