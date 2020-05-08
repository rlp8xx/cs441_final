#!/usr/bin/env python

# This script runs the haskell executable and calculates average times

import subprocess
def run_with_threads(threads=1):
    args = ['./par', "{}".format(threads), "-N {}".format(threads), "WarAndPeace.txt"]
    out = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdout,stderr) = out.communicate()
    stdout = [x for x in stdout.split("\n") if x]
    time = stdout[len(stdout)-1]
    return float(time.split(":")[1].strip())

trials = 3
for threads in [1,2,4,8,16,32,64]:
    total_time = 0
    for trial in range(trials):
        time = run_with_threads(threads)
        total_time += time
        print("Threads: {}, Trial: {}, Time: {}".format(threads,trial,time))
    avg_time = total_time / trials
    print("Average time over {} trials for {} threads is {}".format(trials, threads, avg_time))
