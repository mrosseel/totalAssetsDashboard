#!/bin/sh
python3 assetsDesktop.py >> progress.txt && tail -n 7 progress.txt
