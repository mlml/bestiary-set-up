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

fileh = logging.FileHandler('analysis.log', 'a')
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

        #begin = time.time()
        #q = c.query_graph(c.phone).filter(c.phone.label == 'AA1')
        #q = q.columns(c.phone.id, c.phone.pitch.mean)
        #results = q.all()
        #print(len(results))
        #end = time.time()
        #print('aa query: {} seconds'.format(end - begin))
        beg = time.time()
        discourse = c.discourses[0]
        print(discourse)
        csv_path = 'test.txt'
        q = c.query_graph(c.word).filter(c.word.type_subset == 'of_interest').filter(c.word.name_position > 3)
        q = q.columns(c.word.label.column_name('word'),
                    c.word.name_position.column_name('element_number'),
                    c.word.duration.column_name('duration'),
                    c.word.relativized_duration_by_speaker.column_name('relative_duration'),
                    c.word.pitch.mean.column_name('pitch'),
                    c.word.pitch_relative.mean.column_name('relative_pitch'),
                    c.word.formants.mean.column_name('formants'),
                    c.word.formants_relative.mean.column_name('relative_formants'),
                    c.word.intensity.mean.column_name('intensity'),
                    c.word.intensity_relative.mean.column_name('relative_intensity'),
                    c.word.discourse.name.column_name('discourse'),
                    c.word.speaker.name.column_name('speaker'),
                    )
        results = q.to_csv(csv_path)
        end = time.time()
        logger.info('Query took: {}'.format(end - beg))


if __name__ == '__main__':
    logger.info('Begin processing: {}'.format(name))
    print('hello')
    analysis()
