#!/bin/bash
git clone git@github.com:RuthGnz/SpyScrap.git ./CLI
mv ./CLI/* .
rm -rf CLI 
bash ./setup.sh
pip3 install -r back_requirements.txt
pip3 install -r requirements.txt
rm main.py
rm requirements.txt
rm README.md