from collections import OrderedDict
from datetime import date
from typing import Dict, Mapping, Iterable
from .diary import find_tags, find_ids, iter_entries


def stats(entries: Mapping[date, Iterable]) -> Dict[str, int]:
    output = OrderedDict()  # type: Dict[str, int]
    output['# Days'] = len(entries)
    output['# Entries'] = sum(len(list(v)) for v in entries.values())
    output['# Taggings'] = sum(len(list(find_tags(l)))
                               for d, l, t in iter_entries(entries))
    output['# Identification'] = sum(len(list(find_ids(l)))
                                     for d, l, t in iter_entries(entries))

    for key, val in output.items():
        print('{:.<20}{:.>5}'.format(key, val))

    return output
