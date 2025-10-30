#!/bin/bash

set -euo pipefail

python3 src/main.py
test -d docs
cd docs
python3 -m http.server 8888 