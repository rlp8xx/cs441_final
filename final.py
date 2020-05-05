from multiprocessing import Pool
import functools
import sys
import cProfile

# turns head of list into a dict
# adds following tuples into the dict
def reducer(a, b):
    if type(a) is not dict:
        return reducer({a[0]:a[1]},b)
    else:
        if b[0] in a.keys():
            a[b[0]] = a[b[0]] + b[1]
        else:
            a[b[0]] = b[1]
    return a

def reduce_dict(freq_dict):
    n = len(freq_dict.keys())
    def dict_reducer(a,b):
        return 

    reduced = functools.reduce(dict_reducer, freq_dict)

def mapper(a):
    return (a,1)

def count_occurrences(data):
    mapped = sorted(map(mapper, data))
    reduced = functools.reduce(reducer, mapped)
    return reduced

def main(argv):
    num_threads = int(argv[1])
    filepath = argv[2]

    with open(filepath, "r") as book:
        mystr = book.read()

    # split file into array of lines, remove empty lines
    book_lines = [line for line in mystr.split("\n") if line]

    with Pool(processes=num_threads) as pool:
        occs = pool.map(count_occurrences, book_lines)
    
if __name__ == "__main__":
    main(sys.argv)
