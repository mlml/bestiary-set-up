import sys
PGDB_REPO_PATH = r'D:\Dev\GitHub\PolyglotDB'
AS_REPO_PATH = r'D:\Dev\GitHub\python-acoustic-similarity'

sys.path.insert(0, AS_REPO_PATH)
sys.path.insert(0, PGDB_REPO_PATH)
import os
import time
import logging

import polyglotdb.io as pgio

from polyglotdb import CorpusContext
from polyglotdb.config import CorpusConfig
graph_db = {'graph_host':'localhost', 'graph_port': 7474,
            'graph_user': 'neo4j', 'graph_password': 'test'}

data_dir = r'D:\Data\Dimensions\truncated_aligned'

name = 'three_dimensions'

config = CorpusConfig(name, **graph_db)
config.pitch_algorithm = 'praat'
config.formant_algorithm = 'praat'
config.intensity_algorithm = 'praat'

fileh = logging.FileHandler('sampling.log', 'a')
logger = logging.getLogger('three-dimensions')
logger.setLevel(logging.DEBUG)
logger.addHandler(fileh)

def call_back(*args):
    args = [x for x in args if isinstance(x, str)]
    if args:
        print(' '.join(args))

words = ['megan', 'benjamin', 'marjorie', 'logan', 'marvin', 'lauren',
        'sally','morgan','marion', 'dillon','molly','lilly','jeremy',
        'nolan','sarah','lillian']

def analysis():
    print('hi')
    with CorpusContext(config) as c:
        if False:
            c.query_graph(c.word).filter(c.word.label.in_(words)).set_type('of_interest')
            c.encode_position('utterance', 'word', 'name_position', subset = 'of_interest')
        if True:
            c.encode_relativized('word', 'duration', by_speaker = True)
        beg = time.time()
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.word.label == 'logan').filter(c.phone.discourse.name == 'suborn_1253_7_1')

        q = q.columns(c.phone.word.label.column_name('word'),
                    c.phone.word.name_position.column_name('element_number'),
                    c.phone.label.column_name('phone'),
                    c.phone.begin.column_name('begin'),
                    c.phone.end.column_name('end'),
                    c.phone.duration.column_name('duration'),
                    c.phone.pitch.track.column_name('pitch'),
                    c.phone.discourse.name.column_name('discourse'),
                    c.phone.speaker.name.column_name('speaker'),
                    )
        q.to_csv('track_test.txt')
        print('track query took:', time.time() - beg)

        beg = time.time()
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.word.label == 'logan').filter(c.phone.discourse.name == 'suborn_1253_7_1')

        q = q.columns(c.phone.word.label.column_name('word'),
                    c.phone.word.name_position.column_name('element_number'),
                    c.phone.label.column_name('phone'),
                    c.phone.begin.column_name('begin'),
                    c.phone.end.column_name('end'),
                    c.phone.duration.column_name('duration'),
                    c.phone.pitch.sampled_track.column_name('pitch'),
                    c.phone.discourse.name.column_name('discourse'),
                    c.phone.speaker.name.column_name('speaker'),
                    )
        q.to_csv('sampled_test.txt')
        print('sampled query took:', time.time() - beg)

        beg = time.time()
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.word.label == 'logan').filter(c.phone.discourse.name == 'suborn_1253_7_1')

        q = q.columns(c.phone.word.label.column_name('word'),
                    c.phone.word.name_position.column_name('element_number'),
                    c.phone.label.column_name('phone'),
                    c.phone.begin.column_name('begin'),
                    c.phone.end.column_name('end'),
                    c.phone.duration.column_name('duration'),
                    c.phone.pitch.interpolated_track.column_name('pitch'),
                    c.phone.discourse.name.column_name('discourse'),
                    c.phone.speaker.name.column_name('speaker'),
                    )
        q.to_csv('interpolated_test.txt')
        print('interpolated query took:', time.time() - beg)

if __name__ == '__main__':
    logger.info('Begin processing: {}'.format(name))
    print('hello')
    analysis()
