#!/bin/bash

url=$1
httpurl="http://$url"

cd $PWD

## Put into tmux panes!

tmux new-window -n '--> Web <--'

# bottom left pane
tmux split-window -v
tmux select-pane -t 0
tmux send-keys "nuclei -u $httpurl | tee nuclei" C-m

# top left pane
tmux split-window -h
tmux select-pane -t 1
tmux send-keys \
    "feroxbuster -e -u $httpurl --smart --silent --force-recursion -o feroxbuster && \
    cat feroxbuster | awk '{print $1}' >> urls.txt" C-m

# top right pane
tmux split-window -h
tmux select-pane -t 2
tmux send-keys \
    "katana -u $httpurl -jc -kf all -aff -d 10 -o katana && \
    katana -u $httpurl -jc -kf all -aff -d 10 -f path -o k_paths && \
    katana -u $httpurl -jc -kf all -aff -d 10 -f url -o k_urls && \
    katana -u $httpurl -jc -kf all -aff -d 10 -f udir -o k_dirs && \
    cat k_dirs | sort -u >> urls.txt && \
    cat k_paths | sed 's/^.//g' >> paths.txt" C-m

# below top right
tmux split-window -v
tmux select-pane -t 3
tmux send-keys \
    "arjun -u $httpurl -w /usr/lib/python3/dist-packages/arjun/db/large.txt > arjun && \
    arjun -i urls.txt -w /usr/lib/python3/dist-packages/arjun/db/large.txt >> arjun" C-m
