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

fileh = logging.FileHandler('acoustics.log', 'a')
logger = logging.getLogger('three-dimensions')
logger.setLevel(logging.DEBUG)
logger.addHandler(fileh)

syllabics = ['AA1','AE1','IY1','IH1','EY1','EH1','AH1','AO1',
                            'AW1','AY1','OW1','OY1','UH1','UW1','ER1',
                            'AA2','AE2','IY2','IH2','EY2','EH2','AH2','AO2',
                            'AW2','AY2','OW2','OY2','UH2','UW2','ER2',
                            'AA0','AE0','IY0','IH0','EY0','EH0','AH0','AO0',
                            'AW0','AY0','OW0','OY0','UH0','UW0','ER0']


def call_back(*args):
    args = [x for x in args if isinstance(x, str)]
    if args:
        print(' '.join(args))

def acoustics():
    print('hi')
    with CorpusContext(config) as c:
        c.reset_acoustics()
        beg = time.time()
        c.analyze_acoustics(pitch = True, formants = False, intensity = False)
        end = time.time()
        logger.info('Pitch took: {}'.format(end - beg))

        beg = time.time()
        c.relativize_pitch()
        end = time.time()
        logger.info('Relativizing pitch took: {}'.format(end - beg))

        beg = time.time()
        c.analyze_acoustics(pitch = False, formants = True, intensity = False)
        end = time.time()
        logger.info('Formants took: {}'.format(end - beg))

        beg = time.time()
        c.relativize_formants()
        end = time.time()
        logger.info('Relativizing formants took: {}'.format(end - beg))

        beg = time.time()
        c.analyze_acoustics(pitch = False, formants = False, intensity = True)
        end = time.time()
        logger.info('Intensity took: {}'.format(end - beg))

        beg = time.time()
        c.relativize_intensity()
        end = time.time()
        logger.info('Relativizing intensity took: {}'.format(end - beg))

if __name__ == '__main__':
    logger.info('Begin processing: {}'.format(name))
    print('hello')
    acoustics()
