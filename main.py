#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'runningMedian' function below.
#
# The function is expected to return a DOUBLE_ARRAY.
# The function accepts INTEGER_ARRAY a as parameter.
#
from avl_tree import AVLTree


def runningMedian(a):
    bbtr = AVLTree()
    medians = []
    for val in a:
        bbtr.add(val)
        k = len(bbtr) // 2
        if len(bbtr) % 2 == 1:  # length: 2k + 1
            median = bbtr.kth_val(k)
        else:  # length: 2k
            median = (bbtr.kth_val(k - 1) + bbtr.kth_val(k)) / 2
        medians.append(float(median))
    return medians


if __name__ == "__main__":
    with open(os.environ["INPUT_PATH"], "r") as f, open(os.environ["OUTPUT_PATH"], "w") as fptr:
        a_count = int(f.readline().strip())

        a = []

        for _ in range(a_count):
            a_item = int(f.readline().strip())
            a.append(a_item)

        result = runningMedian(a)

        fptr.write("\n".join(map("{:.1f}".format, result)))
        fptr.write("\n")
