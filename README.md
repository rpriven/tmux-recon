# tmux-recon

I put this here mostly so I can quickly setup my terminal and kali machine with my tmux and ohmytmux config as well as to run my tmux recon scripts.  I hope someone else finds this useful.

## Description

This creates bash aliases for recon and discovery that when run open multiple tmux panes to run various scans and saves the results in your current directory.

## Installation

**WARNING**: This will overwrite your existing .bash_aliases, .tmux.conf and .tmux.conf.local files
Please back them up first or just pick the things you like from them instead of copying over the entire repository

I will eventually have a script to set all this up, but it is pretty simple:

1. Install Oh my tmux! at https://github.com/gpakosz/.tmux
2. Clone this repository to your /home/kali/ directory (or your user directory)

```bash
git clone https://github.com/rpriven/tmux-recon.git
```

3. Modify .tmux.conf and .tmux.conf.local (from Oh my tmux!) or use my versions
4. Add the bash aliases for recon and discovery automation

## Usage

### Recon

This runs several different nmap scans and enum4linux-ng

```bash
recon <ip>
```

### Discover

Enumerates websites:  This runs nuclei, feroxbuster, katana and arjun

```bash
discover <ip>
```

This will be updated as there are quite a few improvements I hope to make that I'm currently testing.

## To Do

- Create an install script that backs up a users current files if existing
- Update the tools and procedures for recon and discover
- Add additional features beyond port scanning and web discovery
