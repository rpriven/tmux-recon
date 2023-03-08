# Bash Aliases for Pentesting Automation

alias a='arsenal -t'

e4l() {
    docker run -t enum4linux-ng -A -C $1
}

wes() {
    cwd=$(basename $PWD)
    if [ ! -f systeminfo.txt ]; then
        echo "Error, no 'systeminfo.txt' file found in '$PWD'"
    else
        cd $HOME/scripts/wesng
        $HOME/scripts/wesng/wes.py $OLDPWD/systeminfo.txt -c -o wes-"$cwd"-vulns.txt
        $HOME/scripts/wesng/wes.py $OLDPWD/systeminfo.txt -c -s critical > wes-"$cwd"-critical.txt
        $HOME/scripts/wesng/wes.py $OLDPWD/systeminfo.txt -c -i "Remote Code Execution" > wes-"$cwd"-rce.txt
        mv wes-"$cwd"-vulns.txt wes-"$cwd"-critical.txt wes-"$cwd"-rce.txt $OLDPWD
        cd $OLDPWD
    fi
}

# Recon
recon() {
    $HOME/scripts/recon.sh $1
}

# recon.sh, enum-smb.sh, enum-web.sh, discover.sh
full() {
    $HOME/scripts/full-recon.sh $1
}

gomap() {
    naabu -host $1 -nmap-cli 'nmap $2'
}

#enum-smb
#enum-web
#enum-api
#enum-owasp

brute-web() {
    $HOME/scripts/brute-web.sh $1
}

# discover directories, files and subdomains
discover() {
    $HOME/scripts/web-recon.sh $1
}
#enum-nginx
nginx-recon() {
    $HOME/scripts/nginx-recon.sh $1
}

# MSF

msfl() {
    msfconsole -r $HOME/scripts/multi_handler.rc
}

# Folder shortcuts
alias htb='cd ~/htb'
alias thm='cd ~/tryhackme'
alias cr='cd ~/cyberranges'
alias scripts='cd $HOME/scripts/'
alias impacket='cd /usr/share/doc/python3-impacket/examples'

new-htb() {
    cd ~/htb
    mkdir $1
    cd $1
}

new-thm() {
    cd $HOME/tryhackme
    mkdir $1
    cd $1
}

new-cr() {
    cd $HOME/cyberranges
    mkdir $1
    cd $1
}

transfer() {
    cd $HOME/transfer
    ls
    python3 -m http.server 80
}


# VPN
alias vpn-htb='sudo openvpn ~/htb/vip21_enphix.ovpn'
alias vpn-thm='sudo openvpn ~/tryhackme/djedi.riven.ovpn'
alias vpn-cr='sudo openvpn ~/cyberranges/enphix-6e020607-4742-4eda-892c-0cd4552a419a.ovpn'
