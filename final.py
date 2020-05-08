from multiprocessing import Pool
from collections import Counter
import functools
import math
import sys
import time

# Recursively group chraracters
def group(size, chars):
    return [chars[i:i+size] for i in range(0, len(chars), size)]

# Insert or update chars in dic
def add_to_dict(dic, chars):
    if not dic:
        dic = {}
    if chars in dic.keys():
        dic[chars] = dic[chars]+1
    else:
        dic[chars] = 1
    return dic

# Split string into roughly `amt_chunks` pieces
def chunk(chars, amt_chunks):
    chunk_size = round(len(chars) / amt_chunks)
    return group(chunk_size, chars)

# Merge two frequency dicts together
def freq_reduce(a, b):
    return dict(Counter(a)+Counter(b))

# Count occurrences in chars or groups of chars
def count(chars):
    # convert chars to counter, return counter as a dict
    return dict(Counter(chars))

# Use map and reduce to count character groups
def count_groups(chars, amt_threads, grp_size):
    chars = group(grp_size, chars)
    chunks = chunk(chars, amt_threads)
    # multithread the counting process
    with Pool(processes=amt_threads) as pool:
        mapped = pool.map(count, chunks)
    return functools.reduce(freq_reduce, mapped)

# Reduce counted groups
def info_reduce(a, b, total):
    p = b / total
    if a is None:
        return (-p) * b * math.log2(p)
    else:
        return a + (-p) * b * math.log2(p)

if __name__ == "__main__":
    with open("WarAndPeace.txt", "r") as infile:
        data = infile.read()
    threads = int(sys.argv[1])
    stime = time.time()
    for size in [1,2,3]:
        # Count groups with 
        counted_groups = count_groups(data, threads, size)
        total_groups = sum(counted_groups.values())
        info = functools.reduce(lambda a, b: info_reduce(a,b,total_groups), counted_groups.values())
    print(time.time()-stime)
