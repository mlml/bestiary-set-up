import sys

# PGDB_REPO_PATH = r'D:\Dev\GitHub\PolyglotDB'
PGDB_REPO_PATH = r'/mnt/d/Dev/GitHub/PolyglotDB'
# AS_REPO_PATH = r'D:\Dev\GitHub\python-acoustic-similarity'
AS_REPO_PATH = r'/mnt/d/Dev/GitHub/python-acoustic-similarity'

sys.path.insert(0, AS_REPO_PATH)
sys.path.insert(0, PGDB_REPO_PATH)
import os
import time
import logging

import polyglotdb.io as pgio

from polyglotdb import CorpusContext
from polyglotdb.config import CorpusConfig

graph_db = {'graph_host': 'localhost', 'graph_port': 7474, 'bolt_port': 7476, 'acoustic_port': 8300,
            'graph_user': 'neo4j', 'graph_password': 'test'}

name = 'three_dimensions'

config = CorpusConfig(name, **graph_db)
config.pitch_source = 'reaper'
config.formant_source = 'praat'
config.intensity_source = 'praat'

fileh = logging.FileHandler('analysis.log', 'a')
logger = logging.getLogger('three-dimensions')
logger.setLevel(logging.DEBUG)
logger.addHandler(fileh)


def call_back(*args):
    args = [x for x in args if isinstance(x, str)]
    if args:
        print(' '.join(args))


words = ['megan', 'benjamin', 'marjorie', 'logan', 'marvin', 'lauren',
         'sally', 'morgan', 'marion', 'dillon', 'molly', 'lilly', 'jeremy',
         'nolan', 'sarah', 'lillian', 'or', 'and']


def analysis():
    print('hi')
    with CorpusContext(config) as c:
        if not c.hierarchy.has_token_property('word', 'name_position'):
            c.query_graph(c.word).filter(c.word.label.in_(words)).set_type('of_interest')
            c.encode_position('utterance', 'word', 'name_position', subset='of_interest')
        print('interest encoded')
        if not c.hierarchy.has_token_property('word', 'relativized_duration_by_speaker'):
            c.encode_relativized('word', 'duration', by_speaker=True)
        print('word relative duration encoded')
        # if not c.hierarchy.has_token_property('phone', 'utterance_position'):
        #    c.encode_position('utterance', 'phone', 'utterance_position')
        # print('phone utterance position encoded')
        if not c.hierarchy.has_token_property('phone', 'relativized_duration_by_speaker'):
            c.encode_relativized('phone', 'duration', by_speaker=True)
        print('phone relative duration encoded')
        if not c.hierarchy.has_token_property('phone', 'word_position'):
            c.encode_position('word', 'phone', 'word_position')
        print('phone word position encoded')
        if not c.hierarchy.has_token_property('word', 'num_phones'):
            c.encode_count('word', 'phone', 'num_phones')
        print('done enrichment')
        # begin = time.time()
        # q = c.query_graph(c.phone).filter(c.phone.label == 'AA1')
        # q = q.columns(c.phone.id, c.phone.pitch.mean)
        # results = q.all()
        # print(len(results))
        # end = time.time()
        # print('aa query: {} seconds'.format(end - begin))
        beg = time.time()
        csv_path = 'pgdb_analysis.txt'
        if not os.path.exists(csv_path):
            q = c.query_graph(c.word).filter(c.word.type_subset == 'of_interest')
            q = q.columns(c.word.label.column_name('word'),
                          c.word.name_position.column_name('element_number'),
                          c.word.duration.column_name('duration'),
                          c.word.relativized_duration_by_speaker.column_name('relative_duration'),
                          c.word.pitch.mean.column_name('pitch'),
                          c.word.pitch_relative.mean.column_name('relative_pitch'),
                          # c.word.formants.mean.column_name('formants'),
                          # c.word.formants_relative.mean.column_name('relative_formants'),
                          c.word.intensity.mean.column_name('intensity'),
                          c.word.intensity_relative.mean.column_name('relative_intensity'),
                          c.word.discourse.name.column_name('discourse'),
                          c.word.speaker.name.column_name('speaker'),
                          )
            q.to_csv(csv_path)
            end = time.time()
            logger.info('Query took: {}'.format(end - beg))

        q = c.query_graph(c.phone).filter(c.phone.word.type_subset == 'of_interest')
        pitch_col = c.phone.pitch.track.column_name('pitch')
        pitch_col.attribute.relative_times = True
        intensity_col = c.phone.intensity_relative.track.column_name('intensity')
        intensity_col.attribute.relative_times = True
        beg = time.time()
        csv_path = 'pitch_tracks.txt'
        if not os.path.exists(csv_path):
            q = q.columns(c.phone.label.column_name('phone'),
                          c.phone.begin.column_name('begin'),
                          c.phone.end.column_name('end'),
                          c.phone.word.name_position.column_name('word_element_number'),
                          c.phone.word.num_phones.column_name('word_num_phones'),
                          # c.phone.utterance_position.column_name('utterance_position'),
                          c.phone.word_position.column_name('word_position'),
                          c.phone.word.label.column_name('word'),
                          pitch_col,
                          # intensity_col,
                          c.phone.discourse.name.column_name('discourse'),
                          c.phone.speaker.name.column_name('speaker'),
                          )
            q.to_csv(csv_path)
            end = time.time()
            logger.info('Query took: {}'.format(end - beg))

        beg = time.time()
        csv_path = 'intensity_tracks.txt'

        if not os.path.exists(csv_path):
            q = c.query_graph(c.phone).filter(c.phone.word.type_subset == 'of_interest')
            q = q.columns(c.phone.label.column_name('phone'),
                          c.phone.begin.column_name('begin'),
                          c.phone.end.column_name('end'),
                          c.phone.word.name_position.column_name('word_element_number'),
                          c.phone.word.num_phones.column_name('word_num_phones'),
                          # c.phone.utterance_position.column_name('utterance_position'),
                          c.phone.word_position.column_name('word_position'),
                          c.phone.word.label.column_name('word'),
                          # pitch_col,
                          intensity_col,
                          c.phone.discourse.name.column_name('discourse'),
                          c.phone.speaker.name.column_name('speaker'),
                          )
            q.to_csv(csv_path)
            end = time.time()
            logger.info('Intensity track query took: {}'.format(end - beg))

        beg = time.time()
        csv_path = 'duration_tracks.txt'
        if not os.path.exists(csv_path):
            q = c.query_graph(c.phone).filter(c.phone.word.type_subset == 'of_interest')
            q = q.columns(c.phone.label.column_name('phone'),
                          c.phone.begin.column_name('begin'),
                          c.phone.end.column_name('end'),
                          c.phone.duration.column_name('duration'),
                          c.phone.relativized_duration_by_speaker.column_name('relative_duration'),
                          c.phone.word.name_position.column_name('word_element_number'),
                          c.phone.word.num_phones.column_name('word_num_phones'),
                          # c.phone.utterance_position.column_name('utterance_position'),
                          c.phone.word_position.column_name('word_position'),
                          c.phone.word.label.column_name('word'),
                          c.phone.discourse.name.column_name('discourse'),
                          c.phone.speaker.name.column_name('speaker'),
                          )
            q.to_csv(csv_path)
            end = time.time()
            logger.info('Duration track query took: {}'.format(end - beg))


if __name__ == '__main__':
    logger.info('Begin processing: {}'.format(name))
    print('hello')
    analysis()
