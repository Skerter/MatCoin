#!/bin/bash

rm -rf bin

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt

buildozer android debug