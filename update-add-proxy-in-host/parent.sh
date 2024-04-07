#!/bin/bash

while read line;
do
    echo "$line" | xargs python update-add-proxy-in-host.py
done < ./hosts.txt
