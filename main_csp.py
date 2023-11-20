import random

from classes import *
from CSP import CSPSolver

TEACHERS_PER_SUBJECT = 2
SUBJECTS_PER_GROUP = 7
LESSONS_PER_DAY = 3


def get_random_subset(items: List, size: int) -> List:
    return random.sample(items, size)


def get_random_subset_of_teachers(teachers: List[Teacher]) -> List[Teacher]:
    return get_random_subset(teachers, TEACHERS_PER_SUBJECT)


def get_random_subset_of_subjects(subjects: List[Subject]) -> List[Subject]:
    return get_random_subset(subjects, SUBJECTS_PER_GROUP)


def main() -> None:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    teachers = [
        Teacher("Cat"),
        Teacher("Fish"),
        Teacher("Rhino"),
        Teacher("Elephant"),
        Teacher("Bird"),
        Teacher("Capybara"),
        Teacher("Parrot"),
        Teacher("Fox"),
    ]
    rooms = [
        Room(215, 30),
        Room(505, 35),
        Room(1, 27),
        Room(39, 100),
        Room(303, 25),
        Room(27, 35),
    ]
    subjects = [
        Subject("Cooking", get_random_subset_of_teachers(teachers)),
        Subject("Singing", get_random_subset_of_teachers(teachers)),
        Subject("Dancing", get_random_subset_of_teachers(teachers)),
        Subject("Running", get_random_subset_of_teachers(teachers)),
        Subject("Sunbathing", get_random_subset_of_teachers(teachers)),
        Subject("Walking", get_random_subset_of_teachers(teachers)),
        Subject("Traveling", get_random_subset_of_teachers(teachers)),
        Subject("Reading", get_random_subset_of_teachers(teachers)),
        Subject("Algorithms", get_random_subset_of_teachers(teachers)),
    ]
    groups = [
        Group("1-A", get_random_subset_of_subjects(subjects), 20),
        Group("1-B", get_random_subset_of_subjects(subjects), 30),
        Group("2-A", get_random_subset_of_subjects(subjects), 26),
    ]

    cnt = 0
    for i in range(100):
        csp_solver = CSPSolver()
        csp_solver.set_variables(groups, days, LESSONS_PER_DAY)
        csp_solver.set_domains(rooms)
        schedule = csp_solver.solve().schedule
        found = len(schedule) > 0
        cnt += not found
    print(f"Not found: {cnt}\n")

    csp_solver = CSPSolver()
    csp_solver.set_variables(groups, days, LESSONS_PER_DAY)
    csp_solver.set_domains(rooms)
    schedule = csp_solver.solve().schedule

    print("=================================\n")

    for main_day in days:
        print(f"[Day: {main_day}]")

        for group, schedule_per_group in schedule.items():
            list_of_classes = schedule_per_group[main_day]
            print(f"  Group: {group.name}")
            for class_ in list_of_classes:
                print(f"  {class_.time.number})")
                print(f"  room = {class_.room.number}")
                print(f"  lesson = {class_.subject.name}")
                print(f"  teacher = {class_.teacher.name}")
            print("  --------------------")
        print("=================================")


if __name__ == '__main__':
    main()
