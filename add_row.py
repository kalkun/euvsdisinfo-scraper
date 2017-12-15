#!/usr/bin/env python3

import sys
c= 0
for line in sys.stdin:
    if c == 0:
        print("row;"+line.strip())
    else:
        print("ost" + str(c) + ";" + line.strip())
    c += 1

