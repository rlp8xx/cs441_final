from multiprocessing import Pool
import functools
import sys
import cProfile

# Recursively group chraracters
def group(size, chars):
    if len(chars) < size:
        return []
    return [chars[0:size]] + group(size, chars[size:])

# Insert or update chars in dic
def add_to_dict(dic, chars):
    if not dic:
        dic = {}
    if chars in dic.keys():
        dic[chars] = dic[chars]+1
    else:
        dic[chars] = 1
    return dic

# Recursively count character groupings into a dict
def count_groups(acc, groups):
    if not groups:
        return acc
    acc = add_to_dict(acc, groups[0])
    if len(groups) > 1:
        return count_groups(acc, groups[1:])
    else:
        return acc

# Split string into roughly `amt_chunks` pieces
def chunk(chars, amt_chunks):
    chunk_size = round(len(chars) / amt_chunks)
    def _chunk(chars):
        if len(chars) < chunk_size:
            return [chars]
        else:
            return [chars[0:chunk_size]] + _chunk(chars[chunk_size:])
    return _chunk(chars)

# Merge two frequency dicts together
def freq_reduce(a, b):
    def _freq_reduce(a, b):
        item = b[0]
        if item[0] in a:
            a[item[0]] = a[item[0]] + item[1]
        else:
            a[item[0]] = item[1]
        if len(b) > 1:
            return _freq_reduce(a, b[1:])
        else:
            return a
    if not b:
        return a
    return _freq_reduce(a, list(b.items())) 

# Do all the processing
def process(chars, amt_chunks):
    chars = group(3, chars)
    chunks = chunk(chars, amt_chunks)
    mapped = map(lambda x: count_groups(None,x), chunks)
    return functools.reduce(freq_reduce, mapped)
