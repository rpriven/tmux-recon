#!/bin/bash

# tmux-recon install script

# if exists, creates backups of configs
if [[ ~/.tmux.conf -f ]]; then
	mv .tmux.conf .tmux.conf.bak && mv .tmux.conf.local .tmux.conf.local.bak
else
	continue
fi

# ohmytmux!
cd
git clone https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf
cp .tmux/.tmux.conf.local .

# tmux-recon
cd
git clone https://github.com/rpriven/tmux-recon.git
mv tmux-recon/scripts tmux-recon/.bash_aliases tmux-recon/.tmux.conf tmux-recon/.tmux.conf.local .

# arsenal
cd
git clone https://github.com/Orange-Cyberdefense/arsenal.git
cd arsenal
python3 -m pip install -r requirements.txt
#./addalias.sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "alias a='${DIR}/run -t'" >> ~/.bash_aliases
echo "alias a='${DIR}/run -t'" >> ~/.zshrc
echo "alias a='${DIR}/run -t'" >> ~/.bashrc
source ~/.bash_aliases
cd

echo "[+] tmux-recon installed"
