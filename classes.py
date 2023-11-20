from typing import List


class Room:
    def __init__(self, number: int, capacity: int):
        self.number = number
        self.capacity = capacity

    def __eq__(self, other):
        return self.capacity == other.capacity and self.number == other.number


class Teacher:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


class Subject:
    def __init__(self, name: str, teachers: List[Teacher]):
        self.name = name
        self.teachers = teachers


class Group:
    counter = 0

    def __init__(self, name: str, subjects: List[Subject], size: int):
        self.id = Group.counter
        Group.counter += 1
        self.name = name
        self.subjects = subjects
        self.size = size

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    def __len__(self):
        return self.size


class Time:
    def __init__(self, day: str, number: int):
        self.day = day
        self.number = number


class Class:

    def __init__(self, class_group: Group, class_subject: Subject, class_room: Room,
                 class_teacher: Teacher, class_time: Time):
        self.group = class_group
        self.subject = class_subject
        self.room = class_room
        self.teacher = class_teacher
        self.time = class_time
