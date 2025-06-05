#!/bin/bash
# Use for local testing
python3 src/main.py -b /
cd docs && python3 -m http.server 8888
