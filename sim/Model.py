class Intersection:
    in_streets = set()
    out_streets = set()

    schedule = []
    cur_green_id = 0
    cur_green_remaining = 0

    queues = {}

    def __init__(self):
        pass

    def add_in_street(self, street):
        self.in_streets.add(street)
        self.queues[street] = []

    def add_out_street(self, street):
        self.out_streets.add(street)

    def set_schedule(self, schedule: list):
        self.schedule = schedule
        # Remove 0-length items
        self.schedule = [x for x in self.schedule if x[1] > 0]
        if len(self.schedule) == 0:
            self.cur_green_id = -1
        else:
            self.cur_green_id = 0
            self.cur_green_remaining = self.schedule[0][1]

    def add_car(self, car):
        self.queues[car.current_street].append(car)

    def sim(self):
        if self.cur_green_id != -1:
            # Check which street is green
            if self.cur_green_remaining == 0:
                if self.cur_green_id == len(self.schedule):
                    self.cur_green_id = 0
                else:
                    self.cur_green_id = self.cur_green_id + 1
                self.cur_green_remaining = self.schedule[self.cur_green_id][1]
            else:
                self.cur_green_remaining = self.cur_green_remaining - 1

            q = self.queues.get(self.schedule[self.cur_green_id][0])
            if len(q) > 0:
                c = q.pop(0)
                if c is not None:
                    c.get_next_street().enter_car(c)


class Street:
    name = None
    length = 0

    start_intersection = None
    end_intersection = None

    traffic = {}

    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length

    def set_start(self, intersection: Intersection):
        self.start_intersection = intersection
        intersection.add_out_street(self)

    def set_end(self, intersection: Intersection):
        self.end_intersection = intersection
        intersection.add_in_street(self)

    def enter_car(self, car):
        car.go_to_next_street()
        self.traffic[car] = self.length

    def sim(self):
        end_car = None

        for c, t in self.traffic.items():
            self.traffic[c] = t - 1
            if t == 1:
                end_car = c

        if end_car is not None:
            del self.traffic[end_car]
            self.end_intersection.add_car(end_car)


class Car:

    route = None
    current_street = None
    current_street_id = 0

    finished = False

    def __init__(self, route):
        self.route = route
        self.current_street_id = 0
        self.current_street = route[0]

    def get_next_street(self):
        return self.route[self.current_street_id+1]

    def go_to_next_street(self):
        self.current_street_id = self.current_street_id+1
        self.current_street = self.route[self.current_street_id]
