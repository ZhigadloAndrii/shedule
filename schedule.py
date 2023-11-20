from typing import Dict
from collections import defaultdict
from random import choice

from classes import *
from input import *


class Schedule:
    def __init__(self):
        self.schedule: Dict[Group, Dict[str, List[Class]]] = defaultdict(lambda: defaultdict(list))

    @staticmethod
    def generate_random_schedule(data: Input) -> 'Schedule':
        schedule_obj = Schedule()
        schedule = schedule_obj.schedule

        for group in data.groups:
            for day in data.days:
                for lesson_num in range(data.lessons_per_day):
                    subject = choice(group.subjects)
                    teacher = choice(subject.teachers)
                    room = Schedule.get_random_room(data.rooms, group.size)
                    schedule[group][day].append(Class(group, subject, room, teacher, Time(day, lesson_num)))

        return schedule_obj

    @staticmethod
    def get_random_room(rooms: List[Room], group_size: int) -> Room:
        filtered_rooms = [room for room in rooms if room.capacity >= group_size]
        return choice(filtered_rooms)
