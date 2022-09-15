import functools
import sys

data = []

for line in sys.stdin:
    if ":" in line or len(line.split()) < 3:
        continue
    if "EOF" in line: break

    data.append(tuple([float(x) for x in line.split()[1:]]))

def closest_pair(data):
    Px = sorted(data, key=lambda x: x[0])
    Py = sorted(data, key=lambda x: x[1])
    closest_pair = closest_pair_aux(Px, Py)
    return dist(closest_pair[0], closest_pair[1])

@functools.cache
def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def min_dist(Px):
    min_pair = (Px[0], Px[1])
    min_dist = dist(min_pair[0], min_pair[1])
    for i in Px:
        for j in Px:
            if i == j: 
                continue
            if dist(i, j) < min_dist:
                min_pair = (i, j)
                min_dist = dist(i, j)
    return min_pair

def closest_pair_aux(Px, Py):
    if len(Px) <= 3:
        return min_dist(Px)
    
    Qx = Px[:len(Px)//2]
    Rx = Px[len(Px)//2:]
    Qy = []
    Ry = []

    for elem in Py:
        if elem[0] <= Qx[-1][0]:
            Qy.append(elem)
        else:
            Ry.append(elem)
    
    (q1, q2) = closest_pair_aux(Qx, Qy)
    (r1, r2) = closest_pair_aux(Rx, Ry)

    q1_q2_dist = dist(q1, q2)
    r1_r2_dist = dist(r1, r2)

    gamma = min(q1_q2_dist, r1_r2_dist)
    L = Qx[-1][0]
    Sy = []

    for elem in Py:
        if abs(elem[0] - L) < gamma:
            Sy.append(elem)
    
    min_pairs_2 = [(0, 0),(1e7, 1e7)]
    min_dist_2 = dist(min_pairs_2[0], min_pairs_2[1])
    for i in range(len(Sy)):
        points = Sy[i + 1: min(len(Sy), (i + 1) + 15)]
        for p in points:
            if dist(Sy[i], p) < min_dist_2:
                min_pairs_2 = (Sy[i], p)
                min_dist_2 = dist(Sy[i], p)
    
    if dist(min_pairs_2[0], min_pairs_2[1]) < gamma:
        return (min_pairs_2[0], min_pairs_2[1])
    elif q1_q2_dist < r1_r2_dist:
        return (q1, q2)
    else:
        return (r1, r2)

print(closest_pair(data))