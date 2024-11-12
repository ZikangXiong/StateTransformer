#!/bin/bash

# Update and install required packages
apt-get update
apt-get install -y wget git zsh curl iputils-ping

# ping www.baidu.com 5 times, and get the average ttl
# if the average ttl is less than 30 ms, then we are in China
# otherwise, we are not in China

ping_result=$(ping -c 5 www.baidu.com 2>/dev/null)

# Check if ping was successful
if [ $? -ne 0 ]; then
    echo "Error: Could not ping www.baidu.com"
    exit 1
fi

# Extract average time from ping statistics and convert to integer
avg_time=$(echo "$ping_result" | grep 'avg' | awk '{print $4}' | cut -d '/' -f 2)
avg_int=${avg_time%.*}  # Remove decimal part

# Compare with threshold using simple integer comparison
if [ "$avg_int" -lt 30 ]; then
    IS_IN_CHINA=true
else
    IS_IN_CHINA=false
fi

echo "Average ping time: ${avg_time}ms"
echo "In China: $IS_IN_CHINA"


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

mkdir -p /root/.ssh
cp -r /tmp/.ssh/* /root/.ssh/
chmod 600 /root/.ssh/*
chmod 700 /root/.ssh

cd /workspace/

if [ ! -d "/workspace/nuplan-devkit" ]; then
    git clone git@github.com:ZikangXiong/nuplan-devkit.git
fi

git config --global --add safe.directory /workspace/StateTransformer
git config --global --add safe.directory /workspace/nuplan-devkit

mkdir -p ~/.pip
echo "[global]" > ~/.pip/pip.conf

if [ "$IS_IN_CHINA" = true ]; then
    # conda
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
    conda config --set show_channel_urls yes
    # pip
    echo "root-user-action=ignore" >> ~/.pip/pip.conf
    echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf
    echo "trusted-host = pypi.tuna.tsinghua.edu.cn" >> ~/.pip/pip.conf
fi