import sys
MFA_REPO_PATH = r'D:\Dev\GitHub\Montreal-Forced-Aligner'

sys.path.insert(0, MFA_REPO_PATH)

from aligner.command_line.align import align_included_model, align_corpus, fix_path, unfix_path


class DummyArgs(object):
    def __init__(self):
        self.num_jobs = 4
        self.fast = False
        self.speaker_characters = 0
        self.verbose = False
        self.clean = True
        self.no_speaker_adaptation = True
        self.debug = False
        self.errors = False
        self.corpus_directory = r'D:\Data\Dimensions\truncated'
        self.output_directory = r'D:\Data\Dimensions\truncated_aligned'
        self.dictionary_path = r'D:\Data\aligner_comp\dictionaries\dictionary_stressed.txt'
        self.temp_directory = r'D:\Data\Dimensions\Temp'
        self.acoustic_model_path = r'D:\Dev\GitHub\mfa-models\english.zip'


def align():
    args = DummyArgs()
    #align_included_model(language, corpus_dir, output_dir, temp_dir,
    #                     args)
    align_corpus(args)

if __name__ == '__main__':
    fix_path()
    align()
    unfix_path()
