from multiprocessing import Pool
from collections import Counter
import functools
import sys

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

# Use map and reduce to count character groups
def count_groups(chars, amt_chunks, grp_size):
    chars = group(grp_size, chars)
    chunks = chunk(chars, amt_chunks)
    mapped = map(lambda x: dict(Counter(x)), chunks)
    return functools.reduce(freq_reduce, mapped)

if __name__ == "__main__":
    with open("WarAndPeace.txt", "r") as infile:
        data = infile.read()
    print(count_groups(data, 4, 1))
