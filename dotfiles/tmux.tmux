# -- TMUX-RECON .tmux.conf --------------------------------------------------------------------

# -- general -------------------------------------------------------------------

setw -g xterm-keys on
set -g history-limit 999999

# -- custom --------------------------------------------------------------------

setenv -g py3 "python3 -c 'import pty;pty.spawn(\"bin/bash\")'"
setenv -g shellexports "export TERM=xterm;stty rows $(tput lines) columns $(tput cols)"

# stabilize reverse shell
bind C-q send $py3 Enter
bind -n C-q send C-z "stty raw -echo" Enter fg Enter reset Enter $shellexports Enter

# This means you just need to hit Ctrl-aqq
# Ctrl-aq is the first binding
# Ctrl-q is the second part

# kripto
# set -g status-right "#{kripto}"

set -g @kripto_id "bitcoin"
set -g @kripto_currency_symbol " "
set -g @kripto_icon "₿ $"
set -g @kripto_ttl 150
set -t @krypto_round "false"

# -- display -------------------------------------------------------------------

set -g status-interval 5      # redraw status line every 5 seconds
set -g visual-activity on

# -- navigation ----------------------------------------------------------------

# Use | instead of _ to split window horizontally
bind | split-window -h

# switch panes using Alt-arrow without prefix
bind -n M-left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# -- urlview -------------------------------------------------------------------

bind U run "cut -c3- ~/.tmux.conf | sh -s _urlview #{pane_id}"


# -- TMUX-RECON .tmux.conf.local  -------------------------------------------------------------------

# -- theming -------------------------------------------------------------------

# tmux_conf_theme_colour_18="#f7931a"   # bitcoin yellow

# -- clipboard -----------------------------------------------------------------

tmux_conf_copy_to_os_clipboard=true

# -- user customizations -------------------------------------------------------

set -g mouse on

# -- tpm -----------------------------------------------------------------------

set -g @plugin 'tmux-plugins/tmux-copycat'
set -g @plugin 'tmux-plugins/tmux-cpu'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'

# -- custom plugins -----------------------------------------------------------

set -g @plugin 'tmux-plugins/tmux-online-status'
set -g @plugin 'xamut/tmux-network-bandwidth'
#set -g @plugin 'ChanderG/tmux-notify'
#set -g @tnotify-verbose 'on'
set -g @plugin 'tmux-plugins/tmux-prefix-highlight'
set -g @plugin 'vascomfnunes/tmux-kripto'
set -g @plugin '27medkamal/tmux-session-wizard'

