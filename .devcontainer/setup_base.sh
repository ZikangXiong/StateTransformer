#!/bin/bash

# Update and install required packages
apt-get update
apt-get install -y wget git zsh curl

# Install oh-my-zsh
chsh -s $(which zsh)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p /root/miniconda3
rm /tmp/miniconda.sh

# Configure conda
echo 'export PATH=/root/miniconda3/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
/root/miniconda3/bin/conda init zsh
/root/miniconda3/bin/conda create -n dev python=3.10 -y
/root/miniconda3/bin/conda clean -a -y