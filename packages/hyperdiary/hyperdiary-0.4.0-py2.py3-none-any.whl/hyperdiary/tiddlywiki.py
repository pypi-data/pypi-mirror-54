import os
import io
import re
import unicodedata
from datetime import date
from typing import Union, Iterable, Iterator, Tuple
from . import diary


def make_tiddler_filename(o: Union[str, date]) -> str:
    '''
    >>> make_tiddler_filename("Frühstück Ähre Grüße Föhn")
    'fruehstueck-aehre-gruesse-foehn.tid'
    >>> make_tiddler_filename("a.v-_'üöß' tiddler")
    'av-_ueoess-tiddler.tid'
    >>> make_tiddler_filename(date(2019, 2, 3))
    '2019-02-03.tid'
    '''
    if isinstance(o, str):
        s = o.lower() \
             .replace('ß', 'ss') \
             .replace('ä', 'ae') \
             .replace('ö', 'oe') \
             .replace('ü', 'ue')
        s = unicodedata.normalize('NFKD', s)
        s = s.encode('ascii', 'ignore').decode('ascii')
        s = re.sub('[^\w\s-]', '', s).strip()
        s = re.sub('[-\s]+', '-', s)
    elif isinstance(o, date):
        s = '{:04d}-{:02d}-{:02d}'.format(o.year, o.month, o.day)
    else:
        raise NotImplementedError('Cannot convert object of type '
                                  '{} to filename'.format(type(o)))
    return '{}.tid'.format(s)


class Tiddler:
    def __init__(self, fname: diary.Pathlike, **fields: str) -> None:
        self.fname = fname
        self.fields = dict(**fields)

    @property
    def title(self) -> str:
        return self.fields['title']

    @property
    def text(self) -> str:
        return self.fields['text']

    def __str__(self) -> str:
        return '<Tiddler(title="{0}")>'.format(self.title)

    def __repr__(self) -> str:
        return 'Tiddler({0})'.format(', '.join(
            '{}="{}"'.format(k, v) for k, v in self.fields.items()))

    def _fields_without_text(self) -> Iterator[Tuple[str, str]]:
        for key, val in self.fields.items():
            if key.lower() != 'text':
                yield key, val

    def to_tid(self) -> str:
        return '\n'.join(['{} = {}'.format(k, v) for k, v in
                          self._fields_without_text()]) \
            + '\ntype: text/vnd.tiddlywik\n\n' \
            + self.text

    def to_div(self) -> str:
        args = ' '.join(['{}="{}"'.format(k, v) for k, v in
                         self._fields_without_text()])
        return '<div {}>\n<pre>\n{}\n</pre>\n</div>'.format(args, self.text)

    @staticmethod
    def from_entry(dt: date, entry: Iterable) -> 'Tiddler':
        tags = []
        day_text = io.StringIO()
        for line in entry:
            day_text.write('* ')
            for token in diary.tokenize(line):
                if token.type == diary.TokenType.Id:
                    day_text.write('[[{}|{}]]'.format(token.text, token.ref))
                elif token.type == diary.TokenType.Text:
                    day_text.write(token.text)
                elif token.type == diary.TokenType.Tag:
                    tags.append(token.text)
                else:
                    raise NotImplementedError('Unknown TokenType')
            day_text.write('\n')
        day_text.seek(0)
        compact_date = '{:04d}{:02d}{:02d}1200000000'.format(dt.year, dt.month,
                                                             dt.day)

        fields = dict(title=nice_date(dt),
                      text=day_text.read(),
                      tags=' '.join(sorted(set(tags))),
                      created=compact_date,
                      modified=compact_date)

        return Tiddler(make_tiddler_filename(dt), **fields)


def nice_date(dt: date) -> str:
    return dt.strftime("%d.%m.%Y")


def diary_to_tiddlers(diary_instance: diary.Diary) -> Iterator[Tiddler]:
    entries = diary_instance.entries
    for dt in sorted(entries.keys()):
        yield Tiddler.from_entry(dt, entries[dt])
    # ToDo: add additional (system) tiddlers
    # yield Tiddler(title='$:/DefaultTiddlers', fname='defaultxxx',
    #               text='[[10.06.2019]]')


def diary_to_tiddlers_export(diary_instance: diary.Diary,
                             tiddler_dir: diary.Pathlike) -> None:
    os.makedirs(str(tiddler_dir), exist_ok=True)
    for tiddler in diary_to_tiddlers(diary_instance):
        with open(os.path.join(str(tiddler_dir), str(tiddler.fname)), 'w') \
                as f:
            f.write(tiddler.to_tid())


_STORE_AREA_SENTINEL = 'id="storeArea"'


def diary_to_tiddlywiki_export(diary_instance: diary.Diary,
                               file: diary.Pathlike,
                               tiddlywiki_base_file: diary.Pathlike) -> None:
    content = '\n'.join(tiddler.to_div() for tiddler in
                        diary_to_tiddlers(diary_instance))
    sentinel_found = False
    with open(str(file), 'w') as f, \
            open(str(tiddlywiki_base_file), 'r') as wiki:
        for line in wiki:
            f.write(line)
            if _STORE_AREA_SENTINEL in line:
                f.write(content)
                sentinel_found = True
    if not sentinel_found:
        raise Exception('Could not find \'{}\' in file {}'
                        .format(_STORE_AREA_SENTINEL, tiddlywiki_base_file))
