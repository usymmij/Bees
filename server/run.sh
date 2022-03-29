#!/bin/bash

ip_addy= curl ifconfig.me
# ip_addy:8080 for node
# ip_addy:6500 for python
python server.py $ip_addy &
node index.js