#!/bin/bash

virtualenv -p python3 myenv
source myenv/bin/activate
pip3 install -r requirements.txt
mkdir reports
cd reports
touch junit.xml
touch cover.xml
touch pep8.report
cd ..
cd sistema_bancario
python3 manage.py jenkins — enable-coverage