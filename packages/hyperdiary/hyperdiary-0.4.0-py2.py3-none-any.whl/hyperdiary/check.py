from .diary import Diary, iter_entries, EntryType


def check(diary: Diary) -> None:
    dates_found = set()
    for dtrange in diary.expected:
        for dt in dtrange:
            if dt not in diary.entries:
                raise Exception('Missing entry {}'.format(dt))
            dates_found.add(dt)

    print('OK found {} days'.format(len(dates_found)))

    dates_with_bad_types = set([])
    for dt, _, entry_type in iter_entries(diary.entries):
        if entry_type != EntryType.Line:
            dates_with_bad_types.add(dt)

    if dates_with_bad_types:
        print('WARNING found {} days with type dict or dict-line '
              '(which is deprecated and support will be removed in '
              'hyperdiary version 0.5):'.format(len(dates_with_bad_types)))
        for dt in dates_with_bad_types:
            print(dt)
