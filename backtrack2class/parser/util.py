WEEK_DAY = [
    'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
    'friday', 'saturday',
]

WEEK_DAY_IND = {day: idx for idx, day in enumerate(WEEK_DAY)}


def split_course_section(course_with_section: str) -> tuple[str, int]:
    lis = course_with_section.split()
    if len(lis) == 1:  # CSE-1101
        return lis[0], 1
    if len(lis) == 2:  # CSE 1101
        return lis[0] + '-' + lis[1], 1
    if len(lis) == 3 and lis[1] == 'Section':  # CSE-1101 Section 1
        return lis[0], int(lis[3])
    if len(lis) == 4 and lis[2] == 'Section':  # CSE 1101 Section 1
        return lis[0] + '-' + lis[1], int(lis[3])
    raise ValueError("invalid course format")


def time_to_minutes(time: str) -> int:
    pst = time[-2:].lower()
    hr, mn = map(int, time[:-2].split(':'))
    return (hr + (12 if pst == 'pm' else 0)) * 60 + mn


def day_time_to_minutes(time: str, day: str) -> int:
    try:
        return time_to_minutes(time) + WEEK_DAY_IND[day.lower()] * 60 * 24
    except KeyError:
        raise ValueError('invalid day')


def time_from_minutes(val: int) -> str:
    hr, mn = val // 60, val % 60
    if hr > 12:
        hr, pst = hr - 12, 'pm'
    elif hr == 0:
        hr, pst = 12, 'am'
    else:
        pst = 'am'
    hr_str = str(hr).zfill(2)
    mn_str = str(mn).zfill(2)
    return f'{hr_str}:{mn_str}{pst}'


def day_time_from_minutes(val: int) -> tuple[str, str]:
    day_idx, val = val // (60 * 24), val % (60 * 24)
    day_str = WEEK_DAY[day_idx].capitalize()
    return time_from_minutes(val), day_str


def conv_schedule_to_seq(a: list[tuple[str, str]], time_unit: int = 1) -> list[int]:
    return sorted([*{
        i for start, end in a
        for i in range(
            time_to_minutes(start) // time_unit,
            (time_to_minutes(end) + time_unit - 1) // time_unit
        )
    }])


def _main():
    print(day_time_from_minutes(60 * 24))
    print(time_to_minutes('1:00pm'), time_to_minutes('2:00pm'), time_to_minutes('12:00am'), time_to_minutes('12:00pm'))
    print(conv_schedule_to_seq([('8:30am', '1:00pm'), ('2:00pm', '5:00pm')], 30))


if __name__ == '__main__':
    _main()
