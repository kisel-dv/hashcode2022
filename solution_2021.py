import random

streets = {}
cars = {}
intersections = {}
schedule = {}
duration = 0
bonus = 0
USED_STREETS = set()
GARBAGE_CARS = set()

class Car:
    def __init__(self, path_len, path, car_id):
        self.car_id = car_id
        self.path_len = path_len
        self.path = path


class Street:
    def __init__(self, start_intersection, end_intersection, name, travel_time):
        self.name = name
        self.start_intersection = start_intersection
        self.end_intersection = end_intersection
        self.travel_time = int(travel_time)
        self.contain_cars = 0


class Intersection:
    def __init__(self):
        self.streets_starting = []
        self.streets_ending = []


class CustomWriter():
    def __init__(self, file):
        self.file = file

    def writeline(self, line):
        self.file.write(f'{line}\n')


def print_res(schedule, file_path):
    with open(file_path, 'w') as f:
        writer = CustomWriter(f)
        writer.writeline(f'{len(schedule)}')
        for k, v in schedule.items():
            writer.writeline(f'{k}')
            writer.writeline(f'{len(v)}')
            for street in v:
                # street name, time
                writer.writeline(f'{street[0]} {street[1]}')


# ----------------------------------------------------------------------------------------------------------------------

# input
def read_file(file_path):
    global duration, intersections_num, streets_num, cars_num, bonus
    with open(file_path, 'r') as f:
        # d, i, s, v, f
        duration, intersections_num, streets_num, cars_num, bonus = map(int, f.readline().strip().split(' '))
        for i in range(streets_num):
            start_intersection, end_intersection, name, travel_time = f.readline().strip().split(' ')
            streets[name] = Street(start_intersection, end_intersection, name, travel_time)
            if not start_intersection in intersections:
                intersections[start_intersection] = Intersection()
            if not end_intersection in intersections:
                intersections[end_intersection] = Intersection()
            intersections[start_intersection].streets_starting.append(name)
            intersections[end_intersection].streets_ending.append(name)
        for i in range(cars_num):
            data = f.readline().strip().split(' ')
            car_path_len = int(data[0])
            car_path = data[1:]
            cars[i] = Car(car_path_len, car_path, i)
            for s in car_path:
                streets[s].contain_cars += 1

    return streets, cars, intersections, schedule


def get_score(schedule):
    cars_num = len(cars)
    available_time = [-1 for _ in range(cars_num)]
    current_roads = [0 for _ in range(cars_num)]
    reach_end = [False for _ in range(cars_num)]

    passed = {s: 0 for s in streets}

    car_number = []
    reached = {s: 0 for s in streets}
    for i in range(cars_num):
        cur_road = cars[i].path[0]
        reached[cur_road] += 1
        car_number.append(reached[cur_road])


    lights = {}
    for i in intersections:
        start = 0
        time_cycle = 0
        for road in schedule[i]:
            time_cycle += road[1]
        for road in schedule[i]:
            lights[road[0]] = [start, start + road[1] - 1, time_cycle]
            start += road[1]


    done, score = 0, 0
    for time in range(duration):
        used_roads = set()
        for car in cars:
            if reach_end[car] or available_time[car] > time:
                continue
            # street_name!
            cur_road = cars[car].path[current_roads[car]]
            if cur_road in used_roads:
                continue

            # TODO: опасный код
            if cur_road in lights:
                green_light = lights[cur_road][0] <= time % lights[cur_road][2] <= lights[cur_road][1]
            else:
                green_light = False

            # print(cur_road, green_light)
            if green_light and passed[cur_road] + 1 == car_number[car]:
                # едем!
                passed[cur_road] += 1

                current_roads[car] += 1
                next_road = cars[car].path[current_roads[car]]
                available_time[car] = time + streets[next_road].travel_time
                used_roads.add(cur_road)

                if available_time[car] > duration:
                    GARBAGE_CARS.add(car)

                if current_roads[car] == cars[car].path_len - 1:
                    if available_time[car] <= duration:
                        done += 1
                        score += bonus + duration - available_time[car]
                        reach_end[car] = True
                else:
                    reached[next_road] += 1
                    car_number[car] = reached[next_road]
    return [score, f'{done}/{len(cars)}']


def get_score_by_lights():
    cars_num = len(cars)
    available_time = [-1 for _ in range(cars_num)]
    current_roads = [0 for _ in range(cars_num)]
    reach_end = [False for _ in range(cars_num)]

    passed = {s: 0 for s in streets}

    car_number = []
    reached = {s: 0 for s in streets}
    for i in range(cars_num):
        cur_road = cars[i].path[0]
        reached[cur_road] += 1
        car_number.append(reached[cur_road])

    road_cycle = {}
    intersections_mods = {}
    intersection_by_road = {}
    for i in intersections:
        if cur_road not in USED_STREETS:
            continue
        cycle_time = 0
        for x in intersections[i].streets_ending:
            if x in USED_STREETS:
                cycle_time += 1

        intersections_mods[i] = {}
        for mod in range(cycle_time):
            intersections_mods[i][mod] = False
        for road in intersections[i].streets_ending:
            intersection_by_road[road] = i
            road_cycle[road] = cycle_time


    # lights = {}
    # for i in intersections:
    #     start = 0
    #     time_cycle = 0
    #     for road in schedule[i]:
    #         time_cycle += road[1]
    #     for road in schedule[i]:
    #         lights[road[0]] = [start, start + road[1] - 1, time_cycle]
    #         start += road[1]


    done, score = 0, 0
    lights = {}
    for time in range(duration):
        used_roads = set()
        for car in cars:
            if reach_end[car] or available_time[car] > time:
                continue
            # street_name!
            cur_road = cars[car].path[current_roads[car]]
            if cur_road in used_roads:
                continue

            if cur_road not in USED_STREETS:
                continue

            if cur_road in lights:
                green_light = lights[cur_road][0] <= time % lights[cur_road][2] <= lights[cur_road][1]
            else:
                tmp_time = time
                intersection = intersection_by_road[cur_road]
                while intersections_mods[intersection][tmp_time % road_cycle[cur_road]]:
                    tmp_time += 1
                intersections_mods[intersection][tmp_time % road_cycle[cur_road]] = True
                lights[cur_road] = [tmp_time % road_cycle[cur_road], tmp_time % road_cycle[cur_road], road_cycle[cur_road]]
                green_light = lights[cur_road][0] <= time % lights[cur_road][2] <= lights[cur_road][1]

            # # TODO: опасный код
            # if cur_road in lights:
            #     green_light = lights[cur_road][0] <= time % lights[cur_road][2] <= lights[cur_road][1]
            # else:
            #     green_light = False

            # print(cur_road, green_light)
            if green_light and passed[cur_road] + 1 == car_number[car]:
                # едем!
                passed[cur_road] += 1

                current_roads[car] += 1
                next_road = cars[car].path[current_roads[car]]
                available_time[car] = time + streets[next_road].travel_time
                used_roads.add(cur_road)

                if available_time[car] > duration:
                    GARBAGE_CARS.add(car)

                if current_roads[car] == cars[car].path_len - 1:
                    if available_time[car] <= duration:
                        done += 1
                        score += bonus + duration - available_time[car]
                        reach_end[car] = True
                else:
                    reached[next_road] += 1
                    car_number[car] = reached[next_road]
    return [score, f'{done}/{len(cars)}']


def get_score_by_lights_2(schedule):
    light_time = {}
    for i in schedule:
        for s in schedule[i]:
            light_time[s[0]] = s[1]


    cars_num = len(cars)
    available_time = [-1 for _ in range(cars_num)]
    current_roads = [0 for _ in range(cars_num)]
    reach_end = [False for _ in range(cars_num)]

    passed = {s: 0 for s in streets}

    car_number = []
    reached = {s: 0 for s in streets}
    for i in range(cars_num):
        cur_road = cars[i].path[0]
        reached[cur_road] += 1
        car_number.append(reached[cur_road])

    road_cycle = {}
    intersections_mods = {}
    intersection_by_road = {}
    for i in intersections:
        if cur_road not in USED_STREETS:
            continue
        cycle_time = 0
        for x in intersections[i].streets_ending:
            if x in USED_STREETS:
                # cycle_time += 1
                cycle_time += light_time[x]

        intersections_mods[i] = {}
        for mod in range(cycle_time):
            intersections_mods[i][mod] = False
        for road in intersections[i].streets_ending:
            intersection_by_road[road] = i
            road_cycle[road] = cycle_time


    # lights = {}
    # for i in intersections:
    #     start = 0
    #     time_cycle = 0
    #     for road in schedule[i]:
    #         time_cycle += road[1]
    #     for road in schedule[i]:
    #         lights[road[0]] = [start, start + road[1] - 1, time_cycle]
    #         start += road[1]


    done, score = 0, 0
    lights = {}
    for time in range(duration):
        used_roads = set()
        for car in cars:
            if reach_end[car] or available_time[car] > time:
                continue
            # street_name!
            cur_road = cars[car].path[current_roads[car]]
            if cur_road in used_roads:
                continue

            if cur_road not in USED_STREETS:
                continue

            if cur_road in lights:
                green_light = lights[cur_road][0] <= time % lights[cur_road][2] <= lights[cur_road][1]
            else:
                cur_road_greenlight_time = light_time[cur_road]
                # не всегда может в расписании остаться вообще дыра в N секунд, которые нам формально нужны, тогда что?

                tmp_time = time
                intersection = intersection_by_road[cur_road]
                while intersections_mods[intersection][tmp_time % road_cycle[cur_road]]:
                    tmp_time += 1
                start_time = tmp_time
                end_time = tmp_time
                while (not intersections_mods[intersection][tmp_time % road_cycle[cur_road]]) and (end_time - start_time < cur_road_greenlight_time - 1) and (start_time % road_cycle[cur_road] <= end_time % road_cycle[cur_road]):
                    intersections_mods[intersection][tmp_time % road_cycle[cur_road]] = True
                    end_time = tmp_time
                    tmp_time += 1
                if end_time % road_cycle[cur_road] < start_time % road_cycle[cur_road]:
                    end_time = road_cycle[cur_road] - 1

                lights[cur_road] = [start_time % road_cycle[cur_road], end_time % road_cycle[cur_road], road_cycle[cur_road]]
                green_light = lights[cur_road][0] <= time % lights[cur_road][2] <= lights[cur_road][1]

            # # TODO: опасный код
            # if cur_road in lights:
            #     green_light = lights[cur_road][0] <= time % lights[cur_road][2] <= lights[cur_road][1]
            # else:
            #     green_light = False

            # print(cur_road, green_light)
            if green_light and passed[cur_road] + 1 == car_number[car]:
                # едем!
                passed[cur_road] += 1

                current_roads[car] += 1
                next_road = cars[car].path[current_roads[car]]
                available_time[car] = time + streets[next_road].travel_time
                used_roads.add(cur_road)

                if available_time[car] > duration:
                    GARBAGE_CARS.add(car)

                if current_roads[car] == cars[car].path_len - 1:
                    if available_time[car] <= duration:
                        done += 1
                        score += bonus + duration - available_time[car]
                        reach_end[car] = True
                else:
                    reached[next_road] += 1
                    car_number[car] = reached[next_road]
    return [score, f'{done}/{len(cars)}']


def make_schedule(iteration):
    global USED_STREETS
    USED_STREETS = set()
    for c in cars:
        if c in GARBAGE_CARS:
            continue
        for s in cars[c].path:
            USED_STREETS.add(s)
    # schedule
    if iteration == 0:
        for i in intersections.keys():
            if len(intersections[i].streets_ending) < 1:
                continue
            schedule[i] = []
            for s in intersections[i].streets_ending:
                if s in USED_STREETS:
                    schedule[i].append([s, 1])
        return schedule
    else:
        for i in intersections:
            if len(intersections[i].streets_ending) < 1:
                continue
            schedule[i] = []
            for s in intersections[i].streets_ending:
                if s in USED_STREETS:
                    # time = 1
                    time = max(streets[s].contain_cars // 20, 1)
                    schedule[i].append([s, time])
        for i in schedule:
            random.shuffle(schedule[i])
        return schedule


def main(file_path):
    # file_path = './data/f.txt'
    read_file(file_path)

    for c in cars:
        for s in cars[c].path:
            USED_STREETS.add(s)

    TOTAL_ITERATIONS = 25
    max_score = 0
    for cur_i in range(TOTAL_ITERATIONS):
        curr_schedule = make_schedule(cur_i)
        score, cars_finished = get_score(curr_schedule)
        if score > max_score:
            # print('Score was updated!')
            # print(score, cars_finished)
            max_score = score

    score, cars_finished = get_score_by_lights()
    if score > max_score:
        max_score = score

    curr_schedule = make_schedule(cur_i)
    score, cars_finished = get_score_by_lights_2(curr_schedule)
    if score > max_score:
        print('upgrade: {}'.format(score-max_score))
        max_score = score
    return max_score


DIR = '../'
files = [DIR + file_name + '.txt' for file_name in ['a', 'b', 'c', 'd', 'e', 'f']]

total_score = 0
for file in files:
    score = main(file)
    total_score += score
    print(f'File: {file}, score: {score}')
print(f'Total score: {total_score}')