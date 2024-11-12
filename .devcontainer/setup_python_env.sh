#!/bin/bash

# Exit on error
set -e

echo "Activating conda environment 'dev'..."
# Source conda to ensure conda activate works in script
source ~/anaconda3/etc/profile.d/conda.sh || source ~/miniconda3/etc/profile.d/conda.sh

# Create a new conda environment
/root/miniconda3/bin/conda create -n dev python=3.10 -y
/root/miniconda3/bin/conda clean -a -y

# Activate the environment
conda activate dev

if [ $? -eq 0 ]; then
    echo "Successfully activated conda environment 'dev'"
else
    echo "Failed to activate conda environment 'dev'"
    exit 1
fi

echo "Installing PyTorch packages..."
pip3 install torch torchvision

echo "Installing other dependencies..."
cd /workspace/StateTransformer
pip install -r requirements.txt
pip install -e . 
pip install aioboto3
pip install retry
pip install aiofiles
pip install bokeh==2.4.1
pip install ipython
pip install ipdb

cd /workspace/nuplan-devkit
pip install -e .