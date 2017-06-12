#!/usr/bin/env python
# -*- coding: utf-8 -*-

import linecache
import random
import sys

file_name = 'train.csv'

# Get number of line in the file.
with open(file_name) as f:
    NUM_LINES_GET = len(f.readlines())

# Choose a random number of a line from the file.
for _ in range(NUM_LINES_GET) :
    sys.stdout.write(linecache.getline(file_name, random.randint(0, NUM_LINES_GET)))

linecache.clearcache()
