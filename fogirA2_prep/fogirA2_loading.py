import time
from datetime import datetime
import os
import sys

sys.path.insert(0, '/mnt/e/Dev/Polyglot/PolyglotDB')
sys.path.insert(0, '/mnt/e/Dev/Tools/python-acoustic-similarity')
import re
import csv
import platform
import polyglotdb.io as pgio

base_dir = os.path.dirname(os.path.abspath(__file__))

from polyglotdb import CorpusContext
from polyglotdb.io.enrichment import enrich_speakers_from_csv, enrich_discourses_from_csv
from polyglotdb.acoustics.formants.refined import analyze_formant_points_refinement

from polyglotdb.utils import ensure_local_database_running
from polyglotdb import CorpusConfig

now = datetime.now()
date = '{}-{}-{}'.format(now.year, now.month, now.day)
duration_threshold = 0.05
nIterations = 1


def call_back(*args):
    args = [x for x in args if isinstance(x, str)]
    if args:
        print(' '.join(args))


def save_performance_benchmark(config, task, time_taken):
    benchmark_folder = os.path.join(base_dir, 'benchmarks')
    os.makedirs(benchmark_folder, exist_ok=True)
    benchmark_file = os.path.join(benchmark_folder, 'benchmarks.csv')
    if not os.path.exists(benchmark_file):
        with open(benchmark_file, 'w', encoding='utf8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['Computer', 'Corpus', 'Date', 'Corpus_size', 'Task', 'Time'])
    with open(benchmark_file, 'a', encoding='utf8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([platform.node(), config.corpus_name, date, get_size_of_corpus(config), task, time_taken])


def reset(config):
    with CorpusContext(config) as c:
        print('Resetting the corpus.')
        c.reset()


def loading(config, corpus_dir, textgrid_format):
    with CorpusContext(config) as c:
        exists = c.exists()
    if exists:
        print('Corpus already loaded, skipping import.')
        return
    if not os.path.exists(corpus_dir):
        print('The path {} does not exist.'.format(corpus_dir))
        sys.exit(1)
    with CorpusContext(config) as c:
        print('loading')

        if textgrid_format == "buckeye":
            parser = pgio.inspect_buckeye(corpus_dir)
        elif textgrid_format == "csv":
            parser = pgio.inspect_buckeye(corpus_dir)
        elif textgrid_format.lower() == "fave":
            parser = pgio.inspect_fave(corpus_dir)
        elif textgrid_format == "ilg":
            parser = pgio.inspect_ilg(corpus_dir)
        elif textgrid_format == "labbcat":
            parser = pgio.inspect_labbcat(corpus_dir)
        elif textgrid_format == "partitur":
            parser = pgio.inspect_partitur(corpus_dir)
        elif textgrid_format == "timit":
            parser = pgio.inspect_timit(corpus_dir)
        else:
            parser = pgio.inspect_mfa(corpus_dir)
        parser.call_back = call_back
        beg = time.time()
        c.load(parser, corpus_dir)
        end = time.time()
        time_taken = end - beg
        print('Loading took: {}'.format(time_taken))
    save_performance_benchmark(config, 'import', time_taken)


def basic_enrichment(config, syllabics, pauses):
    with CorpusContext(config) as g:
        if not 'utterance' in g.annotation_types:
            print('encoding utterances')
            begin = time.time()
            g.encode_pauses(pauses)
            # g.encode_pauses('^[<{].*$', call_back = call_back)
            g.encode_utterances(min_pause_length=0.15)  # , call_back = call_back)
            # g.encode_utterances(min_pause_length = 0.5, call_back = call_back)
            time_taken = time.time() - begin
            print('Utterance enrichment took: {}'.format(time_taken))
            save_performance_benchmark(config, 'utterance_encoding', time_taken)

        if syllabics and 'syllable' not in g.annotation_types:
            print('encoding syllables')
            begin = time.time()
            g.encode_syllabic_segments(syllabics)
            g.encode_syllables('maxonset')
            time_taken = time.time() - begin
            print('Syllable enrichment took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'syllable_encoding', time_taken)

        print('enriching utterances')
        if syllabics and not g.hierarchy.has_token_property('utterance', 'speech_rate'):
            begin = time.time()
            g.encode_rate('utterance', 'syllable', 'speech_rate')
            time_taken = time.time() - begin
            print('Speech rate encoding took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'speech_rate_encoding', time_taken)

        if not g.hierarchy.has_token_property('utterance', 'num_words'):
            begin = time.time()
            g.encode_count('utterance', 'word', 'num_words')
            time_taken = time.time() - begin
            print('Word count encoding took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'num_words_encoding', time_taken)

        if syllabics and not g.hierarchy.has_token_property('utterance', 'num_syllables'):
            begin = time.time()
            g.encode_count('utterance', 'syllable', 'num_syllables')
            time_taken = time.time() - begin
            print('Syllable count encoding took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'num_syllables_encoding', time_taken)

        if syllabics and not g.hierarchy.has_token_property('syllable', 'position_in_word'):
            print('enriching syllables')
            begin = time.time()
            g.encode_position('word', 'syllable', 'position_in_word')
            time_taken = time.time() - begin
            print('Syllable position encoding took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'position_in_word_encoding', time_taken)

        if syllabics and not g.hierarchy.has_token_property('syllable', 'num_phones'):
            begin = time.time()
            g.encode_count('syllable', 'phone', 'num_phones')
            time_taken = time.time() - begin
            print('Phone count encoding took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'num_phones_encoding', time_taken)

        # print('enriching words')
        # if not g.hierarchy.has_token_property('word', 'position_in_utterance'):
        #    begin = time.time()
        #    g.encode_position('utterance', 'word', 'position_in_utterance')
        #    print('Utterance position encoding took: {}'.format(time.time() - begin))

        if syllabics and not g.hierarchy.has_token_property('word', 'num_syllables'):
            begin = time.time()
            g.encode_count('word', 'syllable', 'num_syllables')
            time_taken = time.time() - begin
            print('Syllable count encoding took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'num_syllables_encoding', time_taken)

        print('enriching syllables')
        if syllabics and g.hierarchy.has_type_property('word', 'stresspattern') and not g.hierarchy.has_token_property(
                'syllable',
                'stress'):
            begin = time.time()
            g.encode_stress_from_word_property('stresspattern')
            time_taken = time.time() - begin
            print("encoded stress")
            save_performance_benchmark(config, 'stress_encoding_from_pattern', time_taken)
        elif syllabics and re.search(r"\d", syllabics[0]) and not g.hierarchy.has_type_property('syllable',
                                                                                                'stress'):  # If stress is included in the vowels
            begin = time.time()
            g.encode_stress_to_syllables("[0-9]", clean_phone_label=False)
            time_taken = time.time() - begin
            print("encoded stress")
            save_performance_benchmark(config, 'stress_encoding', time_taken)


def speaker_enrichment(config, speaker_file):
    if not os.path.exists(speaker_file):
        print('Could not find {}, skipping speaker enrichment.'.format(speaker_file))
        return
    with CorpusContext(config) as g:
        if not g.hierarchy.has_speaker_property('gender'):
            begin = time.time()
            enrich_speakers_from_csv(g, speaker_file)
            time_taken = time.time() - begin
            print('Speaker enrichment took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'speaker_enrichment', time_taken)
        else:
            print('Speaker enrichment already done, skipping.')


def discourse_enrichment(config, discourse_file):
    if not os.path.exists(discourse_file):
        print('Could not find {}, skipping discourse enrichment.'.format(discourse_file))
        return
    with CorpusContext(config) as g:
        if not g.hierarchy.has_discourse_property('context'):
            begin = time.time()
            enrich_discourses_from_csv(g, discourse_file)
            time_taken = time.time() - begin
            print('Discourse enrichment took: {}'.format(time.time() - begin))
            save_performance_benchmark(config, 'discourse_enrichment', time_taken)
        else:
            print('Discourse enrichment already done, skipping.')

def formant_acoustic_analysis(config, vowels):
    with CorpusContext(config) as c:
        if c.hierarchy.has_token_property('phone', 'F1'):
            print('Formant acoustics already analyzed, skipping.')
            return
        print('Beginning formant analysis')
        beg = time.time()
        metadata = analyze_formant_points_refinement(c, vowels, duration_threshold=duration_threshold,
                                                     num_iterations=nIterations)
        end = time.time()
        time_taken = time.time() - beg
        print('Analyzing formants took: {}'.format(end - beg))
        save_performance_benchmark(config, 'formant_acoustic_analysis', time_taken)


def pitch_acoustic_analysis(config):
    with CorpusContext(config) as c:
        print('Beginning pitch analysis')
        beg = time.time()
        c.analyze_pitch()
        c.relativize_pitch(by_speaker=True, by_phone=False)
        end = time.time()
        time_taken = time.time() - beg
        print('Analyzing pitch took: {}'.format(end - beg))
        save_performance_benchmark(config, 'pitch_acoustic_analysis', time_taken)

def extract(config):
    with CorpusContext(config) as c:
        q = c.query_graph(c.utterance).columns(c.utterance.speaker.name.column_name('speaker'),
                                               c.utterance.speaker.gender.column_name('speaker_gender'),
                                                c.utterance.discourse.name.column_name('filename'),
                                               c.utterance.discourse.context.column_name('context'),
                                               c.utterance.discourse.item.column_name('item'),
                                               c.utterance.discourse.condition.column_name('condition'),
                                               c.utterance.discourse.contour.column_name('contour'),
                                               c.utterance.word.label.column_name('transcription'),
                                               c.utterance.pitch.track
                                               )
        q.to_csv(os.path.join(base_dir, 'F0_tracks.txt'))

        rel_track = c.utterance.pitch_relative.track
        q = c.query_graph(c.utterance).columns(c.utterance.speaker.name.column_name('speaker'),
                                               c.utterance.speaker.gender.column_name('speaker_gender'),
                                                c.utterance.discourse.name.column_name('filename'),
                                               c.utterance.discourse.context.column_name('context'),
                                               c.utterance.discourse.item.column_name('item'),
                                               c.utterance.discourse.condition.column_name('condition'),
                                               c.utterance.discourse.contour.column_name('contour'),
                                               c.utterance.word.label.column_name('transcription'),
                                               rel_track
                                               )
        q.to_csv(os.path.join(base_dir, 'rel_F0_tracks.txt'))


def get_size_of_corpus(config):
    from polyglotdb.query.base.func import Sum
    with CorpusContext(config) as c:
        c.config.query_behavior = 'other'
        if 'utterance' not in c.annotation_types:
            q = c.query_graph(c.word).columns(Sum(c.word.duration).column_name('result'))
        else:
            q = c.query_graph(c.utterance).columns(Sum(c.utterance.duration).column_name('result'))
        results = q.all()
    return results[0]['result']


if __name__ == '__main__':
    r = True
    corpus_name = 'cont'
    corpus_conf = {'corpus_directory': r'/mnt/e/Data/PolyglotData/cont',
                   'input_format': 'mfa',
                   'speaker_enrichment_file': r'/mnt/e/Data/Cont/speaker.txt',
                   'discourse_enrichment_file': r'/mnt/e/Data/Cont/discourse.txt',
                   'vowel_inventory': ["ER0", "IH2", "EH1", "AE0", "UH1", "AY2", "AW2", "UW1", "OY2", "OY1", "AO0",
                                       "AH2", "ER1", "AW1",
                                       "OW0", "IY1", "IY2", "UW0", "AA1", "EY0", "AE1", "AA0", "OW1", "AW0", "AO1",
                                       "AO2", "IH0", "ER2",
                                       "UW2", "IY0", "AE2", "AH0", "AH1", "UH2", "EH2", "UH0", "EY1", "AY0", "AY1",
                                       "EH0", "EY2", "AA2",
                                       "OW2", "IH1"],
                   'extra_syllabic_segments':[],
                   'pauses':'^<SIL>$'}
    print('Processing...')
    with ensure_local_database_running(corpus_name, port=8080) as params:
        print(params)
        config = CorpusConfig(corpus_name, **params)
        print(config.data_dir)
        config.formant_source = 'praat'
        # Common set up
        if r:
            reset(config)
        loading(config, corpus_conf['corpus_directory'], corpus_conf['input_format'])

        speaker_enrichment(config, corpus_conf['speaker_enrichment_file'])
        discourse_enrichment(config, corpus_conf['discourse_enrichment_file'])

        basic_enrichment(config, corpus_conf['vowel_inventory'] + corpus_conf['extra_syllabic_segments'],
                         corpus_conf['pauses'])

        # Formant specific analysis
        #vowels_to_analyze = corpus_conf['vowel_inventory']
        #formant_acoustic_analysis(config, vowels_to_analyze)
        pitch_acoustic_analysis(config)
        extract(config)
        print('Finishing up!')
