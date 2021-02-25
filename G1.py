import random
from sim.sim import run_sim

for file in ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]:
    with open(file) as fil:
        d, intersection, s, v, f = [int(x) for x in fil.readline().split()]
        streets = []
        for i in range(s):
            b, e, name, l = fil.readline().split()
            streets.append((int(b), int(e), name, int(l)))

        vs = []
        for i in range(v):
            p = fil.readline().split()
            vs.append((int(p[0]), p[1:]))

    random.seed(11)


    def gen_new_random_output(duration):
        d = {}
        for b, e, name, l in streets:
            if e not in d:
                d[e] = []
            # if random.randint(0, 5) == 0:
            #     d[e].append((name, random.randint(0, duration)))
            # else:
            #     d[e].append((name, random.randint(0, 3)))
            d[e].append((name, 1))
        # for e in d:
        #     random.shuffle(d[e])
        return [(e, [(name, s) for name, s in d[e]]) for e in d]


    def print_output(output):
        output = [x for x in output if any(y[1] > 0 for y in x[1])]
        s = [str(len(output))]
        for e, intersection in output:
            r = [x for x in intersection if x[1] > 0]
            assert len(r) > 0
            s.append(str(e))
            s.append(str(len(r)))
            for name, q in r:
                s.append(f"{name} {q}")
        return "\n".join(s)


    print(run_sim(streets, vs, d, f, gen_new_random_output(d)))


    with open(file + ".out", "w") as out_file:
        out_file.write(print_output(gen_new_random_output(d)))
    print(file + " done")

