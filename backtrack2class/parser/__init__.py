from typing import Union

import pandas as pd
import numpy as np

from .util import split_course_section


def parse_teacher_info(file, sheet_name: Union[str, int]) -> pd.DataFrame:
    info: pd.DataFrame = pd.read_excel(file, sheet_name=sheet_name, header=0, index_col=0)
    info.index.names = ['Teacher']
    return info


def parse_teacher_courses(file, sheet_name: Union[str, int]) -> pd.DataFrame:
    rev_courses: pd.DataFrame = pd.read_excel(file, sheet_name=sheet_name, header=0)
    rev_courses_lis = rev_courses.apply(lambda x: x.dropna().tolist(), axis=1).tolist()
    courses_lis = [
        [teacher, *split_course_section(course)]
        for teacher, *courses in rev_courses_lis
        for course in courses
    ]
    courses = pd.DataFrame(courses_lis, columns=['Teacher', 'Course', 'Section'])
    courses['Section'] = courses['Section'].astype(np.int8)
    courses['Total Sections'] = courses['Course'].map(
        courses[['Course', 'Section']].groupby('Course').max()['Section']
    ).astype(np.int8)
    return courses


def parse_teacher_schedule(file, sheet_name: Union[str, int]) -> pd.DataFrame:
    schedule: pd.DataFrame = pd.read_excel(file, sheet_name=sheet_name, header=0, index_col=0)
    schedule_dict = schedule.where(pd.notnull(schedule), None).to_dict()
    conv_schedule_lis = [
        [teacher, start, end, day]
        for day, day_schedule in schedule_dict.items()
        for teacher, range_seq_str in day_schedule.items()
        for start, end in map(
            lambda x: x.split('-'),
            range_seq_str.split(';') if range_seq_str is not None else []
        )
    ]
    conv_schedule = pd.DataFrame(conv_schedule_lis, columns=['Teacher', 'Start', 'End', 'Day'])
    conv_schedule = conv_schedule.set_index('Teacher')
    return conv_schedule


def parse_course_info(file, sheet_name: Union[str, int]) -> pd.DataFrame:
    courses: pd.DataFrame = pd.read_excel(file, sheet_name=sheet_name, header=0, index_col=0)
    return courses


def parse_course_options(file, sheet_name: Union[str, int]) -> pd.DataFrame:
    course_options: pd.DataFrame = pd.read_excel(file, sheet_name=sheet_name, header=0, index_col=0)
    return course_options


def parse_student_schedule(file, sheet_name: Union[str, int]) -> pd.DataFrame:
    schedule: pd.DataFrame = pd.read_excel(file, sheet_name=sheet_name, header=0)
    schedule_dict = schedule.where(pd.notnull(schedule), None).to_dict(orient='list')
    conv_schedule_lis = [
        [start, end, day]
        for day, [day_schedule] in schedule_dict.items()
        for start, end in map(
            lambda x: x.split('-'),
            day_schedule.split(';') if day_schedule is not None else []
        )
    ]
    conv_schedule = pd.DataFrame(conv_schedule_lis, columns=['Start', 'End', 'Day'])
    return conv_schedule


def _main():
    import os
    schedule = parse_student_schedule(os.path.join(os.getcwd(), 'data/static_input.xlsx'), 'StudentSchedule')
    print(schedule)


if __name__ == '__main__':
    _main()


