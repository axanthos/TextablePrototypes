from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Processor import Processor

import urllib2

import re

base_url = 'http://www.theatre-classique.fr/pages/programmes/PageEdition.php'

segmenter = Segmenter()
processor = Processor()

try:
    response = urllib2.urlopen(base_url)
    base_html = unicode(response.read(), 'iso-8859-1')   
except urllib2.HTTPError:
    raise ValueError("Couldn't access theatre-classique website")
 
base_html_seg = Input(base_html)

table_seg = segmenter.import_xml(
    segmentation=base_html_seg, 
    element='table', 
    conditions={'id': re.compile(r'^table_AA$')},
    remove_markup=False,
)

line_seg = segmenter.import_xml(
    segmentation=table_seg, 
    element='tr',
    remove_markup=False,
)

field_regex = re.compile(
    r"^\s*<td>\s*<a.+?>(.+?)</a>\s*</td>\s*"
    r"<td>(.+?)</td>\s*"
    r"<td.+?>\s*<a.+?>\s*(\d+?)\s*</a>\s*</td>\s*"
    r"<td.+?>\s*(.+?)\s*</td>\s*"
    r"<td.+?>\s*<a\s+.+?t=\.{2}/(.+?)'>\s*HTML"
)

play_seg = segmenter.tokenize(
    segmentation=line_seg,
    regexes=[
        (field_regex, 'Tokenize', {'author': '&1'}),
        (field_regex, 'Tokenize', {'title': '&2'}),
        (field_regex, 'Tokenize', {'year': '&3'}),
        (field_regex, 'Tokenize', {'genre': '&4'}),
        (field_regex, 'Tokenize', {'url': '&5'}),
    ],
    import_annotations=False,
)

author_list = processor.count_in_context(
    units={'segmentation': play_seg, 'annotation_key': 'author'}
).to_sorted(row={'key_id': '__unit__'}).col_ids

year_list = processor.count_in_context(
    units={'segmentation': play_seg, 'annotation_key': 'year'}
).to_sorted(row={'key_id': '__unit__'}).col_ids

genre_list = processor.count_in_context(
    units={'segmentation': play_seg, 'annotation_key': 'genre'}
).to_sorted(row={'key_id': '__unit__'}).col_ids

titles_seg, _ = segmenter.select(
    segmentation=play_seg,
    regex=re.compile(r'CORNEILLE'),
    annotation_key='author',
)

print "\n".join(s.annotations['title'] for s in titles_seg)
