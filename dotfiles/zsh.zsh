# ---- TMUX-RECON zsh.zsh ----

# source custom aliases if exists
[ -f ~/.aliases.sh ] && source ~/.aliases.sh

# add .scripts to path
export PATH="$HOME/.scripts:$PATH"

# zoxide (if installed)
if command -v zoxide &> /dev/null; then
    eval "$(zoxide init zsh)"
fi

# fzf (if installed)
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# starship (optional fancy prompt)
[ -f ~/.config/starship.toml ] && eval "$(starship init zsh)"

# Custom prompt options or PS1 here if desired

# You can add any shared settings, completions, etc.
