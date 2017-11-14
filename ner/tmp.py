#!/usr/bin/env python3

# Print every location name flattened

import sys

for line in sys.stdin:
    if not line or line.strip() == "": continue
    for token in line.split(","):
        tmp = token.strip().replace('"', '')
        if tmp == "US": tmp = "USA"
        print(tmp)
