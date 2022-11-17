import os

from redscare import Parser, RedScare

# from tqdm import tqdm


# list of all files from data/ directory
datafiles = [
    (f, os.path.getsize(f"data/{f}")) for f in os.listdir("data") if f.endswith(".txt")
]

outfile = ["filename, none, some, many, few, alternate"]

for idx, (datafile, size) in enumerate(datafiles):
    print(f"{idx+1}/{len(datafiles)} - Processing {datafile}")

    if size > 1000000:
        print("Skipping large file")
        continue

    p = Parser(datafile)
    G, s, t = p.G, p.s, p.t
    r = RedScare(G, s, t)
    none, some, many, few, alternate = r.all()
    outfile.append(f"{datafile}, {none}, {some}, {many}, {few}, {alternate}")

# sort all lines except the first one according to the 0th column
outfile = outfile[:1] + sorted(outfile[1:], key=lambda x: x.split(",")[0])

with open("results.csv", "w") as f:
    for line in outfile:
        f.write(f"{line}\n")
