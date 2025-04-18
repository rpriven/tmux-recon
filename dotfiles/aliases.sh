# ~/.scripts/aliases.sh

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ll='ls -lah'
alias la='ls -A'

# Git
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'

# System
alias update='sudo apt update && sudo apt upgrade -y'
alias ports='netstat -tulnp'
alias grep='grep --color=auto'

# Recon / CTF
alias psg='ps aux | grep -i'   # process grep
alias sniff='sudo tcpdump -i any -n'

# Networking
alias myip='curl ifconfig.me'
alias localip="ip a | grep inet"

# Convenience
alias c='clear'
alias h='history'
alias please='sudo $(fc -ln -1)'  # rerun last command with sudo

