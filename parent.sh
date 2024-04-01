#!/bin/bash

for i in $(seq 1 10)
do
    python create-host.py  host$i
done
