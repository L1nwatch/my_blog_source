#!/bin/bash
set -e
# Install related software
sudo apt-get update
sudo apt-get install nginx
sudo apt-get install supervisor
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9
sudo apt-get install python3.9-dev
sudo apt-get install python3.9-venv
sudo apt install python3.9-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py
sudo python3.9 -m pip install virtualenv