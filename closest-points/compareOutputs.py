import glob
import subprocess
import sys
import math

files = glob.glob("data/*tsp.txt")
output = "data/closest-pair-out.txt"

answers = {}

with open(output) as w:
    for l in w:
        answers[l.split()[0].split("/")[-1][:-5]] = float(l.split()[-1])

for f in files:
    ''' pipe file into python3 script and catch the output'''
    p = subprocess.Popen("cat {} | python3 src/cp.py".format(f), shell=True, stdout=subprocess.PIPE)
    name = f.split("/")[-1][:-8]
    output = float(p.stdout.read())
    withinThreshold = abs(answers[name] - output) < 0.001
    if withinThreshold:
        print("✅ ", end="")
    else:
        print("❌ ", end="")
    print("{}: ground truth: {} answer: {}".format(name, answers[name], output))