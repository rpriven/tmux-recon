#!/bin/bash

##### TO DO #####
# Need to write nmap script in python

# Also consider adding:
# rpcdump
# ldapsearch

red=$'\e[1;31m'
green=$'\e[1;32m'
blue=$'\e[1;34m'
bold=$'\e[1m'
norm=$'\e[21m'
reset=$'\e[0m'

greenplus='\e[1;33m[+]\e[0m'
greenstar='\e[1;33m[*]\e[0m'
greenminus='\e[1;33m[-]\e[0m'
redminus='\e[1;31m[-]\e[0m'
redexclaim='\e[1;31m[!]\e[0m'

url=$1
httpurl="http://$url"

cd $PWD

tmux new-window -n '<<Recon>>'

# bottom left pane
tmux split-window -v
tmux select-pane -t 0
tmux send-keys "naabu -host $url -nmap-cli 'nmap -A -T4 -oA nmap' && echo -e '\n\n$greenstar Starting Second Scan... $greenstar\n\n' && naabu -host $url -nmap-cli 'nmap -sV -sC -Pn -oN nmap_sCsV'" C-m

# top left pane
tmux split-window -h
tmux select-pane -t 1
tmux send-keys "naabu -host $url -nmap-cli 'nmap --script vuln -Pn -oN nmap_vuln' && echo -e '\n\n$greenstar Starting Second Scan... $greenstar\n\n' && nmap -A -n -T4 -p- $url -oN nmap_full" C-m

# top right pane
tmux split-window -h
tmux select-pane -t 2
tmux send-keys "docker run -t enum4linux-ng -A -C $url -oY enum4linux-ng" C-m

wait
tmux wait-for Recon

echo "Tmux scans complete"
echo "Parsing data..."
echo "Running additional commands..."
