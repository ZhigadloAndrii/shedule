import random
from typing import List

from classes import Teacher, Room, Subject, Group
from schedule import Schedule
from input import Input
from population import Population

MUTATION_RATE = 0.02
POPULATION_SIZE = 50
EVOLUTION_MAX_ITERATIONS = 5000000

TEACHERS_PER_SUBJECT = 7
SUBJECTS_PER_GROUP = 6
LESSONS_PER_DAY = 4


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

    data = Input(groups, subjects, rooms, teachers, days, LESSONS_PER_DAY)

    population = Population(data, MUTATION_RATE, POPULATION_SIZE)

    iterations = 0

    while not population.answer_ready and iterations < EVOLUTION_MAX_ITERATIONS:
        iterations += 1
        population.evolve()
        if iterations % 100 == 0:
            print(iterations)

    print(f"population size = {POPULATION_SIZE}")
    print(f"mutation rate = {MUTATION_RATE}")
    print(f"iterations = {iterations}")
    print(f"answer is ready = {population.answer_ready}\n\n\n")

    schedule: Schedule = population.get_answer().schedule.schedule

    print("=================================\n")

    for mainDay in days:
        print("[Day: {}]".format(mainDay))

        for group, schedulePerGroup in schedule.items():
            list_of_classes = schedulePerGroup[mainDay]
            print("  Group: {}".format(group.name))
            for class_ in list_of_classes:
                print("  {}: ".format(class_.time.number + 1))
                print("  room = {}".format(class_.room.number))
                print("  lesson = {}".format(class_.subject.name))
                print("  teacher = {}".format(class_.teacher.name))
            print("  --------------------")
        print("=================================")


if __name__ == "__main__":
    main()
