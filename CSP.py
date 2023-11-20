from typing import List, Dict, Optional
import random

from classes import *
from schedule import *


class Variable:
    def __init__(self, id_: int, time_: Time, group_: Group) -> None:
        self.id = id_
        self.time = time_
        self.group = group_

    def __lt__(self, other: 'Variable') -> bool:
        return self.id < other.id


class Domain:
    def __init__(self, subject_: Subject, teacher_: Teacher, room_: Room) -> None:
        self.subject = subject_
        self.teacher = teacher_
        self.room = room_


class CSPSolver:
    def __init__(self) -> None:
        self.kLESSONS_PER_DAY = 0
        self.variables_storage = []
        self.free_variables = set()
        self.domains_storage = []
        self.domains = {}
        self.tmp = {}
        self.variable_neighbours = {}

    def set_variables(self, groups: List[Group], days: List[str], LESSONS_PER_DAY: int) -> None:
        self.kLESSONS_PER_DAY = LESSONS_PER_DAY
        num = 0
        for day in days:
            for lesson in range(1, LESSONS_PER_DAY + 1):
                start = num
                for group in groups:
                    self.variables_storage.append(Variable(num, Time(day, lesson), group))
                    self.free_variables.add(self.variables_storage[-1])
                    num += 1
                finish = num - 1
                for i in range(start, finish + 1):
                    for j in range(start, finish + 1):
                        if i != j:
                            self.variable_neighbours.setdefault(self.variables_storage[i], []).append(
                                self.variables_storage[j])

    def set_domains(self, rooms: List[Room]) -> None:
        for variable in self.variables_storage:
            for subject in variable.group.subjects:
                for teacher in subject.teachers:
                    for room in rooms:
                        self.domains_storage.append(Domain(subject, teacher, room))
                        self.domains.setdefault(variable, []).append(self.domains_storage[-1])
            random.shuffle(self.domains[variable])

    @staticmethod
    def convert_to_schedule(cur: Dict[Variable, Domain]) -> Schedule:
        schedule = Schedule()

        for variable, domain in cur.items():
            num = variable.time.number
            sz = len(schedule.schedule[variable.group][variable.time.day])
            schedule.schedule[variable.group][variable.time.day].extend([None] * (num - sz))
            schedule.schedule[variable.group][variable.time.day][num - 1] = Class(
                variable.group,
                domain.subject,
                domain.room,
                domain.teacher,
                variable.time,
            )

        return schedule

    def solve(self) -> Schedule:
        cur, ans = {}, {}
        self.backtracking(cur, ans)
        return self.convert_to_schedule(ans)

    def mrv_heuristic(self, cur: Dict[Variable, Domain]) -> Variable:
        inf = 1e9
        mn = inf
        res = None
        for variable in self.free_variables:
            cnt = len(self.domains[variable])
            if cnt < mn:
                res = variable
                mn = cnt
        return res

    def degree_heuristic(self, cur: Dict[Variable, Domain]) -> Variable:
        inf = 1e9
        mx = -inf
        res = None
        for variable in self.free_variables:
            cnt = 0
            if mx >= len(self.variable_neighbours[variable]):
                continue
            k = 0
            for variable1 in self.variable_neighbours[variable]:
                k += 1
                if variable1 not in cur:
                    cnt += 1
                if cnt + (len(self.variable_neighbours[variable]) - k) <= mx:
                    break
            if cnt > mx:
                res = variable
                mx = cnt
        return res

    def select_unassigned_variable(self, cur: Dict[Variable, Domain]) -> Optional[Variable]:
        for variable in self.free_variables:
            return variable
        return None

    @staticmethod
    def order_domain_values(domains: List[Domain]) -> List[Domain]:
        # random.shuffle(domains)
        return domains

    # def check_constraints(self, cur: Dict[Variable, Domain]) -> bool:
    #     for variable1, domain1 in cur.items():
    #         for variable2 in self.variable_neighbours[variable1]:
    #             if variable2 in cur:
    #                 domain2 = cur[variable2]
    #                 if domain1.teacher == domain2.teacher:
    #                     return False
    #                 if domain1.room == domain2.room:
    #                     return False
    #     return True

    def check_constraints(self, cur: Dict[Variable, Domain], variable1: Variable, domain1: Domain) -> bool:
        for variable2 in self.variable_neighbours[variable1]:
            if variable2 in cur:
                domain2 = cur[variable2]
                if domain1.teacher == domain2.teacher:
                    return False
                if domain1.room == domain2.room:
                    return False
        return True

    def backtracking(self, cur: dict, ans: dict) -> bool:
        if len(cur) == len(self.variables_storage):
            ans.clear()
            ans.update(cur)
            return True

        variable = self.mrv_heuristic(cur)
        # variable = self.select_unassigned_variable(cur)
        # variable = self.degree_heuristic(cur)
        self.free_variables.discard(variable)

        for domain in self.order_domain_values(self.domains[variable]):
            if self.check_constraints(cur, variable, domain):
                cur[variable] = domain
                self.forward_checking(variable, domain, cur)

                if self.backtracking(cur, ans):
                    return True

                cur.pop(variable)
                self.un_remove_inconsistent_domains(variable)

        self.free_variables.add(variable)
        return False

    def remove_inconsistent_domains(self, variable: Variable, domain: Domain,
                                    cur: Dict[Variable, Domain]) -> None:
        for variable2 in self.variable_neighbours[variable]:
            if variable2 not in cur:
                i = 0
                while i < len(self.domains[variable2]):
                    domain2 = self.domains[variable2][i]
                    if domain.teacher == domain2.teacher or domain.room == domain2.room:
                        self.domains[variable2][i], self.domains[variable2][-1] = self.domains[variable2][-1], self.domains[variable2][i]
                        self.tmp.setdefault(variable2, []).append(self.domains[variable2].pop())
                    else:
                        i += 1

    def un_remove_inconsistent_domains(self, variable: Variable) -> None:
        for variable2 in self.variable_neighbours[variable]:
            for i in range(len(self.tmp.setdefault(variable2, []))):
                self.domains[variable2].append(self.tmp[variable2][i])

    def forward_checking(self, variable: Variable, domain: Domain, cur: Dict[Variable, Domain]) -> None:
        self.remove_inconsistent_domains(variable, domain, cur)

    def least_constraining_value_heuristic(self, variable: Variable, cur_domains: List[Domain]) -> List[Domain]:
        # random.shuffle(self.domains[variable])
        return sorted(cur_domains, key=lambda x: calc_score(variable, x))


def calc_score(variable: Variable, domain: Domain) -> int:
    return len(domain.subject.teachers)
