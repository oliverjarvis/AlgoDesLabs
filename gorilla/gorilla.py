import re
import sys
from itertools import combinations

def blosum(file):

    with open(file) as f:
        hep = True
        data = {}
        for line in f:
            if "#" in line:
                continue
            if hep:
                letters = line.split()
                hep = False
                continue
            l = line.split()
            data[l[0]] = [int(x) for x in l[1:]]

    return letters, data


def parser():

    file = sys.stdin.readlines()
    data = {}
    for line in file:
        if ">" in line:
            name = line.split()[0][1:]
            data[name] = []
        else:
            data[name] = data[name] + [*line.strip()] 
    return data


def get_pairs(file):
    with open(file) as f:
        pairs = []
        for line in f:
            if bool(re.search(r'\d', line)):
                names = line.split()[0][:-1]
                names = names.split("--")
                pairs.append((names[0],names[1]))
    return pairs

def get_cost(a,b):
    index = letters.index(b)
    return costs[a][index]

def find_min_cost(pair):
    # Create empty memo array
    seq_1, seq_2 = data[pair[0]], data[pair[1]]
    m, n = len(seq_1), len(seq_2)
    memo = [[None for _ in range(n + 1)] for x in range(m + 1)]
    list_of_action = ["diff","gap_i","gap_j"]

    # Base condition: opt(0,j) = opt(i,0) = i*delta
    delta = -4
    for j in range(n+1):
        memo[0][j] = (j*delta, "gap_j")
    for i in range(m+1):
        memo[i][0] = (i*delta, "gap_i")
    
    for i in range(1,m+1):
        for j in range(1,n+1):

            # page 282 (6.16)
            # costs[seq_1[i-1], letters.index(seq_2[j-1])] + memo[i-j][j-1][0]
            values = (get_cost(seq_1[i-1],seq_2[j-1]) + memo[i-1][j-1][0], # no action
                    delta + memo[i-1][j][0], # insert gap in first string (i)
                    delta + memo[i][j-1][0]) # insert gap in second string (j)

            m = max(values)
            action = list_of_action[values.index(m)]

            memo[i][j] = (m, action)

    return memo

def recreate_seq(memo):
    seq_1, seq_2 = data[pair[0]], data[pair[1]]
    new_seq_1, new_seq_2 = "", ""
    i, j = len(memo)-1, len(memo[0])-1

    while not [i,j] == [0,0]: 
        action = memo[i][j][1]

        if action == "diff":
            # New letters 
            a, b = seq_1[i-1], seq_2[j-1]
            # Insert in front
            new_seq_1 = a + new_seq_1
            new_seq_2 = b + new_seq_2

            i -= 1
            j -= 1

        elif action == "gap_i":
            # New letters 
            a, b = seq_1[i-1], "-"
            # Insert in front
            new_seq_1 = a + new_seq_1
            new_seq_2 = b + new_seq_2

            i -= 1
        
        elif action == "gap_j":
            # New letters 
            a, b = "-", seq_2[j-1]
            # Insert in front
            new_seq_1 = a + new_seq_1
            new_seq_2 = b + new_seq_2

            j -= 1

    return new_seq_1, new_seq_2

# Getting the letter index and costs
letters, costs = blosum("data/BLOSUM62.txt")

data = parser()
#pairs = get_pairs("data/Toy_FASTAs-out.txt")
pairs = list(combinations(data.keys(), 2))

for pair in pairs:
    # Filling out the table
    memo = find_min_cost(pair)

    # Highest value
    max_val = memo[-1][-1][0]

    # Recreate path
    seq_1, seq_2 = recreate_seq(memo)

    print(f"{pair[0]}--{pair[1]}: {max_val}\n{seq_1}\n{seq_2}")




    
    


