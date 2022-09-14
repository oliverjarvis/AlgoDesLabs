import sys

data = []

for line in open("algdes-labs/algdes-labs/closest-points/data/brd14051-tsp.txt"):
    if ":" in line or len(line.split()) < 3:
        continue
    data.append([float(x) for x in line.split()[1:]])

def closest_pair(data):
    Px = sorted(data, key=lambda x: x[0])
    Py = sorted(data, key=lambda x: x[1])
    closest_pair = closest_pair_aux(Px, Py)
    return print(closest_pair[0][0], closest_pair[0][1], closest_pair[1][0], closest_pair[1][1])

def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def min_dist(Px):
    min_pair = (Px[0], Px[1])
    for i in Px:
        for j in Px:
            if i == j: 
                continue
            if dist(i, j) < dist(min_pair[0], min_pair[1]):
                min_pair = (i, j)
    return min_pair

def closest_pair_aux(Px, Py):
    if len(Px) <= 3:
        return min_dist(Px)
    
    Qx = Px[:len(Px)//2]
    Qy = Py[:len(Py)//2]
    Rx = Px[len(Px)//2:]
    Ry = Py[len(Py)//2:]

    (q1, q2) = closest_pair_aux(Qx, Qy)
    (r1, r2) = closest_pair_aux(Rx, Ry)

    gamma = min(dist(q1, q2), dist(r1, r2))
    L = Qx[-1][0]
    Sy = []

    for elem in Py:
        if abs(elem[0] - L) < gamma:
            Sy.append(elem)
    
    min_pairs_2 = [(0, 0),(1e7, 1e7)]
    for i in range(len(Sy)):
        points = Sy[i + 1: min(len(Sy), (i + 1) + 15)]
        for p in points:
            if dist(Sy[i], p) < dist(min_pairs_2[0], min_pairs_2[1]):
                min_pairs_2 = (Sy[i], p)
    
    if dist(min_pairs_2[0], min_pairs_2[1]) < gamma:
        return (min_pairs_2[0], min_pairs_2[1])
    elif dist(q1, q2) < dist(r1, r2):
        return (q1, q2)
    else:
        return (r1, r2)

closest_pair(data)