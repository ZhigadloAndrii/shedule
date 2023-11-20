import random

from dna import *
from schedule import *
from classes import *


class Population:
    def __init__(self, data: Input, mutation_rate: float, population_size: int):
        self.data = data
        self.mutation_rate = mutation_rate
        self.answer_ready = False
        self.answer = None
        self.population = [DNA(Schedule.generate_random_schedule(data)) for _ in range(population_size)]
        self.calc_fitness()

    def calc_fitness(self):
        sum_fitness = 0.0
        for dna in self.population:
            fitness = dna.calc_fitness()
            if fitness < 0:
                self.answer_ready = True
                self.answer = dna
                return
            sum_fitness += fitness

        for dna in self.population:
            dna.fitness = dna.fitness / sum_fitness

    def evolve(self):
        new_population = []
        for _ in range(len(self.population)):
            dna1 = self.get_dna_with_probability(random.random())
            dna2 = self.get_dna_with_probability(random.random())
            new_population.append(self.mutation(self.crossover_dna(dna1, dna2)))
        self.population = new_population
        self.calc_fitness()

    def mutation(self, dna: DNA) -> DNA:
        for group, schedule_per_group in dna.schedule.schedule.items():
            for day, classes in schedule_per_group.items():
                for i, class_ in enumerate(classes):
                    if random.random() < self.mutation_rate:
                        class_.room = Schedule.get_random_room(self.data.rooms, len(group))
                    if random.random() < self.mutation_rate:
                        class_.teacher = random.choice(class_.subject.teachers)
                    if random.random() < self.mutation_rate:
                        class_.subject = random.choice(group.subjects)
                        class_.teacher = random.choice(class_.subject.teachers)
        return dna

    def crossover(self, class1: Class, class2: Class) -> Class: # +
        # res = Class()
        time = class1.time
        group = class2.group
        room = None
        teacher = None
        subject = None
        if random.random() < 0.5:
            room = class1.room
        else:
            room = class2.room

        if random.random() < 0.5:
            teacher = class1.teacher
        else:
            teacher = class2.teacher

        if random.random() < 0.5:
            subject = class1.subject
            teacher = class1.teacher
        else:
            subject = class2.subject
            teacher = class2.teacher

        return Class(group, subject, room, teacher, time)

    def crossover_dna(self, dna1: DNA, dna2: DNA) -> DNA: # +
        schedule1 = dna1.schedule.schedule
        schedule2 = dna2.schedule.schedule
        dna = DNA(Schedule())
        for group in schedule1:
            if random.random() < 0.5:
                dna.schedule.schedule[group] = self.crossover_schedule_per_group(schedule1[group], schedule2[group])
            else:
                dna.schedule.schedule[group] = self.crossover_schedule_per_group(schedule2[group], schedule1[group])
        return dna

    def crossover_schedule_per_group(self, schedule_per_group1: Dict[str, List[Class]],
                                     schedule_per_group2: Dict[str, List[Class]]) -> Dict[str, List[Class]]: # +
        res = {}

        for day in schedule_per_group1:
            if random.random() < 0.5:
                res[day] = self.crossover_classes(schedule_per_group1[day], schedule_per_group2[day])
            else:
                res[day] = self.crossover_classes(schedule_per_group2[day], schedule_per_group1[day])
        return res

    def crossover_classes(self, classes1: List[Class], classes2: List[Class]) -> List[Class]:
        classes = []
        border = random.randint(0, len(classes1))
        for i in range(border):
            classes.append(self.crossover(classes1[i], classes2[i]))
        for i in range(border, len(classes2)):
            classes.append(self.crossover(classes2[i], classes1[i]))
        return classes

    def get_dna_with_probability(self, probability: float) -> DNA:
        population = self.population
        total_fitness = sum(dna.fitness for dna in population)
        partial_sum = 0.0
        for dna in population:
            partial_sum += dna.fitness / total_fitness
            if probability <= partial_sum:
                return dna
        raise ValueError("No DNA with the given probability was found in the population.")

    def answer_ready(self) -> bool:
        return self.answer_ready

    def get_answer(self) -> DNA:
        return self.answer