#!/usr/bin/python

import random
import sys

"""
usage: python gen.py {matrix_size} {max_element_value}
return: A | b matrix, where rank A = {matrix_size}
"""

f = open('input.txt', 'w')
n = int(sys.argv[1])
f.write('{}\n'.format(n))
for i in range(n):
    for j in range(n+1):
        template = '{} ' if j != n else '{}\n'
        f.write(template.format(random.randint(1, int(sys.argv[2]))))
f.close()
