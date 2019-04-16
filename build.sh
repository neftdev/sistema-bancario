#!/bin/bash

virtualenv -p python3 myenv
source myenv/bin/activate
pip3 install -r requirements.txt
cd ..
cd sistema_bancario
python3 manage.py jenkins — enable-coverage