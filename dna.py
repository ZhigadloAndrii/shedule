from schedule import Schedule


class DNA:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule
        self.fitness = 0.0

    def calc_fitness(self) -> float:
        conflicts_cnt = 0
        schedule = self.schedule.schedule

        for group1, schedulePerGroup1 in schedule.items():
            for group2, schedulePerGroup2 in schedule.items():
                if group1 == group2 or group1 < group2:
                    continue
                for day, listOfClasses in schedulePerGroup1.items():
                    for i in range(len(listOfClasses)):
                        if schedule[group1][day][i].room == schedule[group2][day][i].room:
                            conflicts_cnt += 1
                        if schedule[group1][day][i].teacher == schedule[group2][day][i].teacher:
                            conflicts_cnt += 1

        if conflicts_cnt == 0:
            self.fitness = -1.0
        else:
            self.fitness = 1.0 / conflicts_cnt
        return self.fitness
