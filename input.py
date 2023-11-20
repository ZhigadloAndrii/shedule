from typing import List

from classes import Group, Subject, Room, Teacher


class Input:
    def __init__(self,
                 groups_: List[Group],
                 subjects_: List[Subject],
                 rooms_: List[Room],
                 teachers_: List[Teacher],
                 days_: List[str],
                 lessons_per_day: int):
        self.groups = groups_
        self.subjects = subjects_
        self.rooms = rooms_
        self.teachers = teachers_
        self.days = days_
        self.lessons_per_day = lessons_per_day
