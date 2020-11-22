#!/bin/sh
cd `dirname $0`
conda init
conda activate autolabeling
python main.py