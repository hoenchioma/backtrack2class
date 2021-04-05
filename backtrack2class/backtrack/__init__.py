from bisect import bisect_left
from functools import reduce

from .util import update_dict, set_union, set_intersection
from ..types import Course, Teacher, Student, Routine, RoutineEntry, TimeRange, Schedule


def in_schedule(schedule: list[int], time: int):
    ind: int = bisect_left(schedule, time)
    return ind < len(schedule) and schedule[ind] == time


def is_placeable(day: list[int], start_idx: int, class_len: int):
    end_idx = start_idx + class_len - 1
    if end_idx >= len(day):
        return False
    start = day[start_idx]
    end = day[end_idx]
    return end - start == end_idx - start_idx


def solve(courses_info: dict[Course, tuple[int, int, list[Teacher], list[Student]]],
          teacher_schedules: dict[Teacher, Schedule],
          schedule: Schedule,
          limit: int = -1):
    # optimizing parameters
    for i in range(len(schedule)):
        schedule[i][:] = set_intersection(reduce(
            set_union, (teacher_schedules[teacher][i] for teacher in teacher_schedules)
        ), schedule[i])
        for teacher, teacher_schedule in teacher_schedules.items():
            teacher_schedule[i][:] = set_intersection(teacher_schedule[i], schedule[i])

    # state variables
    courses_in_day = [
        list(filter(
            lambda course: any(
                teacher_schedules[teacher][i]
                for teacher in courses_info[course][2]
            ), courses_info.keys()
        )) for i in range(len(schedule))
    ]
    classes_done_in_day: tuple[set[Course]] = tuple(set() for _ in range(len(schedule)))
    classes_left: dict[Course, int] = {course: no_of_classes for course, (no_of_classes, *_) in courses_info.items()}
    active_teachers: set[Teacher] = set()
    active_students: set[Student] = set()
    to_remove_teacher: tuple[list[list[Teacher]]] = tuple([[] for _ in i] for i in schedule)
    to_remove_student: tuple[list[list[Student]]] = tuple([[] for _ in i] for i in schedule)
    cur_res: Routine = Routine()  # current result/routine
    # res: list[Routine] = []  # list of all correct results/routines

    res_cnt = 0

    def backtrack(time_idx: int = 0, day_idx: int = 0, course_idx: int = 0):
        nonlocal res_cnt

        if limit != -1 and res_cnt >= limit:
            pass

        elif not classes_left:  # no classes left to assign (solution reached)
            res_cnt += 1
            # res.append(Routine(*(cur_res_day.copy() for cur_res_day in cur_res)))
            yield Routine(*(cur_res_day.copy() for cur_res_day in cur_res))

        elif day_idx == len(schedule):  # end of week
            pass

        else:
            day = schedule[day_idx]

            if time_idx == len(day) or len(courses_in_day[day_idx]) == 0:  # end of day
                if day_idx + 1 < len(schedule):
                    # before going to next day trim course space
                    tmp = courses_in_day[day_idx + 1]  # backup
                    courses_in_day[day_idx + 1] = list(filter(lambda x: x in classes_left, courses_in_day[day_idx + 1]))
                    yield from backtrack(0, day_idx + 1)  # move to next day
                    courses_in_day[day_idx + 1] = tmp

            else:
                to_remove_teacher_in_day = to_remove_teacher[day_idx]
                to_remove_student_in_day = to_remove_student[day_idx]

                if course_idx < len(courses_in_day[day_idx]):
                    course = courses_in_day[day_idx][course_idx]
                    no_of_classes, class_len, course_teachers, course_students = courses_info[course]
                    if (
                            course not in classes_done_in_day[day_idx] and  # hasn't already had class today
                            course in classes_left and  # course has non assigned classes
                            is_placeable(day, time_idx, class_len) and  # required time to fit class is available
                            all(i not in active_teachers for i in course_teachers) and  # course teachers are not busy
                            all(i not in active_students for i in course_students) and  # course students are not busy
                            all(  # fits in course teacher's schedule
                                in_schedule(teacher_schedules[teacher][day_idx], time)
                                for teacher in course_teachers
                                for time in range(day[time_idx], day[time_idx] + class_len)
                            )
                    ):
                        start = day[time_idx]
                        end = day[time_idx] + class_len - 1
                        end_idx = time_idx + class_len - 1

                        cur_res[day_idx].append(RoutineEntry(course, TimeRange(start, end)))
                        classes_done_in_day[day_idx].add(course)
                        update_dict(classes_left, course, -1)
                        for teacher in course_teachers:
                            active_teachers.add(teacher)
                            to_remove_teacher_in_day[end_idx].append(teacher)
                        for student in course_students:
                            active_students.add(student)
                            to_remove_student_in_day[end_idx].append(student)

                        yield from backtrack(time_idx, day_idx, course_idx + 1)  # move to next course

                        for student in course_students:
                            to_remove_student_in_day[end_idx].pop()
                            active_students.remove(student)
                        for teacher in course_teachers:
                            to_remove_teacher_in_day[end_idx].pop()
                            active_teachers.remove(teacher)
                        update_dict(classes_left, course, +1)
                        classes_done_in_day[day_idx].remove(course)
                        cur_res[day_idx].pop()

                    yield from backtrack(time_idx, day_idx, course_idx + 1)

                else:  # all courses checked
                    for teacher in to_remove_teacher_in_day[time_idx]:
                        active_teachers.remove(teacher)
                    for student in to_remove_student_in_day[time_idx]:
                        active_students.remove(student)

                    yield from backtrack(time_idx + 1, day_idx)  # move to time step

                    for student in to_remove_student_in_day[time_idx]:
                        active_students.add(student)
                    for teacher in to_remove_teacher_in_day[time_idx]:
                        active_teachers.add(teacher)

    yield from backtrack()


def _main():
    res = (solve(
        courses_info={
            Course('CA', 1): (2, 1, ['TA'], [Student(1, 1), Student(1, 2)]),
            Course('CB', 1): (2, 1, ['TB'], [Student(1, 1), Student(1, 2)]),
            Course('CC', 1): (2, 2, ['TA'], [Student(1, 1)]),
            Course('CD', 1): (1, 2, ['TB'], [Student(1, 2)]),
        },
        teacher_schedules={
            'TA': Schedule(
                sunday=[1, 2, 3],
                monday=[2, 3, 4],
            ),
            'TB': Schedule(
                sunday=[2, 3, 4],
                monday=[1, 2, 3],
            ),
        },
        schedule=Schedule(
            sunday=[0, 1, 2, 3, 4, 5],
            monday=[0, 1, 2, 3, 4, 5],
        ),
    ))
    for i, sol in enumerate(res):
        print('Solution', i)
        for j in sol:
            if len(j) > 0:
                print('----------------------------------')
                print(*j, sep='\n')
                print('----------------------------------')
        print('\n\n')


if __name__ == '__main__':
    _main()
