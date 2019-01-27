#!/bin/bash

sudo apt-get update -y
sudo apt install python-pip
pip install --user pipenv

sudo apt-get dist-upgrade -y
sudo apt-get install -y libreadline-dev libsqlite3-dev libssl-dev libbz2-dev tk-dev

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
exec $SHELL -l

sudo apt-get install libffi-dev
pyenv install 3.7.2