from typing import NamedTuple


class Course(NamedTuple):
    code: str
    section: int = 1


class Student(NamedTuple):
    year: int
    section: int


Teacher = str


class TimeRange(NamedTuple):
    start: int
    end: int


class RoutineEntry(NamedTuple):
    course: Course
    time_range: TimeRange


class Routine(NamedTuple):
    sunday: list[RoutineEntry] = []
    monday: list[RoutineEntry] = []
    tuesday: list[RoutineEntry] = []
    wednesday: list[RoutineEntry] = []
    thursday: list[RoutineEntry] = []
    friday: list[RoutineEntry] = []
    saturday: list[RoutineEntry] = []


DaySchedule = list[int]


class Schedule(NamedTuple):
    sunday: DaySchedule = []
    monday: DaySchedule = []
    tuesday: DaySchedule = []
    wednesday: DaySchedule = []
    thursday: DaySchedule = []
    friday: DaySchedule = []
    saturday: DaySchedule = []
