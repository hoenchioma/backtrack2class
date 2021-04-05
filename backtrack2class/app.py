from . import parser, backtrack
from .parser.logic import calc_student_sections, calc_course_classes, conv_teacher_schedule, conv_student_schedule
from .parser.util import time_from_minutes, WEEK_DAY
from .types import Course


def run(input_file: str, static_input_file: str):
    # input file
    teachers = parser.parse_teacher_info(input_file, 0)
    teacher_courses = parser.parse_teacher_courses(input_file, 1)
    teacher_schedule = parser.parse_teacher_schedule(input_file, 2)

    # static input file
    courses_info = parser.parse_course_info(static_input_file, 'Courses')
    course_options = parser.parse_course_options(static_input_file, 'CourseOptions')
    student_schedule = parser.parse_student_schedule(static_input_file, 'StudentSchedule')

    time_unit: int = 30

    courses = [
        Course(*i) for i in teacher_courses[['Course', 'Section']].drop_duplicates().itertuples(index=False, name=None)
    ]
    course_total_sections = teacher_courses.groupby(['Course'])['Total Sections'].apply(max).to_dict()

    course_teachers = teacher_courses.groupby(['Course', 'Section'])['Teacher'].apply(list).to_dict()
    course_students = calc_student_sections(courses, course_total_sections, courses_info, course_options)
    course_classes = calc_course_classes(courses, courses_info, course_options, time_unit)

    courses_info_inp = {
        course: (*course_classes[course], course_teachers[course], course_students[course])
        for course in courses
    }
    teacher_schedule_inp = conv_teacher_schedule(teacher_schedule, time_unit)
    # print(teacher_schedule_inp)
    schedule_inp = conv_student_schedule(student_schedule, time_unit)
    # print(schedule_inp)

    import sys
    sys.setrecursionlimit(100000)

    res = backtrack.solve(courses_info_inp, teacher_schedule_inp, schedule_inp, 100)

    for i, schedule in enumerate(res):
        print('----------------------------------', 'Schedule', i + 1, '----------------------------------')
        for j, day_schedule in enumerate(schedule):
            print(WEEK_DAY[j].capitalize(), '=', [
                (tuple(course), (time_from_minutes(start * time_unit), time_from_minutes((end + 1) * time_unit)))
                for course, (start, end) in day_schedule
            ])
        print()

