from collections import defaultdict
from math import lcm

from .util import WEEK_DAY_IND, conv_schedule_to_seq
from ..types import Course, Student, Teacher, Schedule

import pandas as pd


def get_class_info(course_type: str, credit: float, time_unit: int = 1) -> tuple[int, int]:
    if course_type == 'Theory':
        if credit == 2.00:
            return 2, 60 // time_unit
        elif credit == 3.00:
            return 2, 90 // time_unit
        else:
            raise ValueError(
                f'credit of {credit} not supported for theory course'
            )
    elif course_type == 'Lab':
        if credit == 0.75:
            return 1, 180 // time_unit
        elif credit == 1.5:
            return 1, 180 // time_unit
        elif credit == 3.0:
            return 2, 180 // time_unit
        else:
            raise ValueError(
                f'credit of {credit} not supported for lab course'
            )
    else:
        raise ValueError(
            f'course type {course_type} not supported'
        )


def calc_course_classes(courses: list[Course],
                        courses_info: pd.DataFrame,
                        course_options: pd.DataFrame,
                        time_unit: int = 1) -> dict[Course, tuple[int, int]]:
    course_classes = {}

    for course in courses:
        course_code, section = course
        try:
            course_type, credit = courses_info.loc[course_code][['Type', 'Credit']]
        except KeyError:
            option = course_options.loc[course_code]['Option']
            course_type, credit = courses_info.loc[option][['Type', 'Credit']]
        course_classes[course] = get_class_info(course_type, credit, time_unit)

    return course_classes


def calc_student_sections(courses: list[Course],
                          course_total_sections: dict[Course, int],
                          courses_info: pd.DataFrame,
                          course_options: pd.DataFrame) -> dict[Course, list[Student]]:
    year_sections = defaultdict(lambda: 1)
    option_sections = defaultdict(int)

    for course_code, total_sections in course_total_sections.items():
        try:
            student_year = courses_info.loc[course_code]['Year']
            year_sections[student_year] = lcm(year_sections[student_year], total_sections)
        except KeyError:
            option = course_options.loc[course_code]['Option']
            option_sections[option] += total_sections

    for option, total_sections in option_sections.items():
        student_year = courses_info.loc[option]['Year']
        year_sections[student_year] = lcm(year_sections[student_year], total_sections)

    section_cnt = defaultdict(lambda: 1)
    res: dict[Course, list[Student]] = {}
    for course_code, section in courses:
        course = Course(course_code, section)
        total_sections = course_total_sections[course_code]
        try:
            student_year = courses_info.loc[course_code]['Year']
            no_of_student_sections = year_sections[student_year] // total_sections
            res[course] = []
            for i in range(no_of_student_sections):
                res[course].append(Student(student_year, section_cnt[course_code]))
                section_cnt[course_code] += 1
        except KeyError:
            option = course_options.loc[course_code]['Option']
            student_year = courses_info.loc[option]['Year']
            no_of_student_sections = year_sections[student_year] // option_sections[option]
            res[course] = []
            for i in range(no_of_student_sections):
                res[course].append(Student(student_year, section_cnt[option]))
                section_cnt[option] += 1

    return res


def conv_teacher_schedule(teacher_schedule: pd.DataFrame, time_unit: int = 1) -> dict[Teacher, Schedule]:
    teacher_schedule['Range'] = teacher_schedule[['Start', 'End']].agg(tuple, axis=1)
    tmp_dict = teacher_schedule.groupby(['Teacher', 'Day'])['Range'].apply(list).to_dict()
    # print(teacher_schedule.groupby(['Teacher', 'Day'])['Range'].apply(list))
    tmp_res = defaultdict(lambda: [[] for _ in range(7)])
    for (teacher, day), day_schedule in tmp_dict.items():
        tmp_res[teacher][WEEK_DAY_IND[day.lower()]] = conv_schedule_to_seq(day_schedule, time_unit)
    res = {
        teacher: Schedule(*day_schedule)
        for teacher, day_schedule in tmp_res.items()
    }
    return res


def conv_student_schedule(student_schedule: pd.DataFrame, time_unit: int = 1) -> Schedule:
    student_schedule['Range'] = student_schedule[['Start', 'End']].agg(tuple, axis=1)
    tmp_dict = student_schedule.groupby('Day')['Range'].apply(list).to_dict()
    tmp_res = [[] for _ in range(7)]
    for day, day_schedule in tmp_dict.items():
        tmp_res[WEEK_DAY_IND[day.lower()]] = conv_schedule_to_seq(day_schedule, time_unit)
    res = Schedule(*tmp_res)
    return res
