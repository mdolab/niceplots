#!/bin/bash
set -e

for f in *.py
do
    echo "Testing $f"
    python "$f"
done