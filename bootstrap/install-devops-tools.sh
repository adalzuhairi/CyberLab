#!/bin/bash

echo "======================================"
echo " CyberLab Bootstrap"
echo "======================================"

sudo apt update

sudo apt install -y \
git \
curl \
wget \
tree \
jq \
unzip \
python3 \
python3-pip

echo ""
echo "Installation terminée."
