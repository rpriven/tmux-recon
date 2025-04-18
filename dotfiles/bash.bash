# ---- TMUX-RECON bash.bash ----

# source custom aliases if exists
[ -f ~/.aliases.sh ] && source ~/.aliases.sh

# add .scripts to path
export PATH="$HOME/.scripts:$PATH"

# zoxide (if installed)
if command -v zoxide &> /dev/null; then
    eval "$(zoxide init bash)"
fi

# fzf (if installed)
[ -f ~/.fzf.bash ] && source ~/.fzf.bash

# Custom prompt options or PS1 here if desired
