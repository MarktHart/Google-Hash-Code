from sim.sim import run_sim

file = "a.txt"

with open(file) as fil:
    # Read file
    d, intersection, s, v, f = [int(x) for x in fil.readline().split()]
    intersections = []
    for i in range(s):
        b, e, name, l = fil.readline().split()
        intersections.append((int(b), int(e), name, int(l)))

    vs = []
    for i in range(v):
        p = fil.readline().split()
        vs.append((int(p[0]), p[1:]))

    run_sim(intersections, vs)
