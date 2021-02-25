from sim.Model import Intersection, Street, Car


def run_sim(ins, vs, time, points, schedule):
    intersections = []
    streets = {}
    cars = []

    # Determine the number of intersections
    max_intersection = 0
    for (a,b,c,d) in ins:
        if a > max_intersection:
            max_intersection = a
        if b > max_intersection:
            max_intersection = b

    # Create intersections
    for i in range(max_intersection+1):
        intersections.append(Intersection())

    # Create streets
    for (start, end, name, length) in ins:
        s = Street(name, length)
        s.set_start(intersections[start])
        s.set_end(intersections[end])
        streets[name] = s

    # Create cars
    for r in vs:
        route = []
        for s in r[1]:
            route.append(streets.get(s))
        c = Car(route)
        c.current_street.end_intersection.add_car(c)

    # Set schedule
    # output = [("intersection id", [("straatnaam", int(s))])]
    for (inter_id, s) in schedule:
        obj_schedule = []
        for (name, time) in s:
            obj_schedule.append((streets[name], time))
        intersections[inter_id].set_schedule(obj_schedule)


    # Run simulation
    t = 0
    while t <= time:
        t += 1
        for i in intersections:
            i.sim()
        for name in streets:
            streets[name].sim()

        # Count finished cars
        finished = 0
        for c in cars:
            if c.current_street is None:
                finished += 1
        if finished == len(cars):
            break

    score = time-t
    finished = 0
    for c in cars:
        if c.current_street is None:
            finished += 1
    score += finished*points

    return score
