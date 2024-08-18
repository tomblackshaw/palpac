#!/bin/bash

for i in 15 14 13 12 11 10 9 8; do
    if which python3.$i &> /dev/null; then
        python3.$i cachespeech.py "$@"
        exit $?
    fi
done
echo "I COULD NOT FIND A COMPATIBLE PYTHON3 INTERPRETER"
exit 1
