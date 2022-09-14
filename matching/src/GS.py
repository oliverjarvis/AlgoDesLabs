from collections import deque
import sys

def match(data):
    n, names, free_men, preferences = data

    woman_rankings = [[None for _ in range(n)] for _ in range(n)]
    for i, w_prefs in enumerate(preferences[1::2]):
        for j, pref in enumerate(w_prefs):
            woman_rankings[i][pref//2] = j

    man_index = lambda x: (x) // 2
    woman_index = lambda x: (x - 1) // 2
    engaged_to = [None] * n * 2

    def prefers_new(woman, current_man, new_man):
        return woman_rankings[woman_index(woman)][man_index(current_man)] > woman_rankings[woman_index(woman)][man_index(new_man)]

    while free_men:
        man = free_men.popleft()
        woman = preferences[man].popleft()

        if engaged_to[woman] == None:
            engaged_to[woman] = man
            engaged_to[man] = woman
        elif prefers_new(woman, engaged_to[woman], man):
            old_man = engaged_to[woman]
            engaged_to[old_man] = None
            free_men.append(old_man)
            engaged_to[woman] = man
            engaged_to[man] = woman
        else:
            free_men.append(man)


    for a in engaged_to[::2]:
        print(f"{names[engaged_to.index(a)]} -- {names[a]}")

def parseData(filename):
    file = open(filename)

    for line in file:
        if line.startswith("n="):
            n = int(line[2:])
            break
    
    names = []
    free_men = deque([i for i in range(n*2)[::2]])
    preferences = [None for _ in range(n * 2)]

    for i in range(n*2):
        line = next(file) + ""
        names.append(line.split()[1])

    next(file)

    for i in range(n*2):
        line = next(file)
        splitline = line.split()
        preferences[int(splitline[0][:-1]) - 1] = deque(preferences[int(splitline[0][:-1]) - 1])
    
    return (n, names, free_men, preferences)


if __name__ == "__main__":
    if len(sys.argv) > 0:
        data = parseData("algdes-labs/matching/data/sm-kt-p-5-in.txt")
        match(data)