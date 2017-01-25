import sys
MFA_REPO_PATH = r'D:\Dev\GitHub\Montreal-Forced-Aligner'

sys.path.insert(0, MFA_REPO_PATH)

from aligner.command_line.align import align_included_model, align_corpus


class DummyArgs(object):
    def __init__(self):
        self.num_jobs = 4
        self.fast = False
        self.speaker_characters = 0
        self.verbose = False
        self.clean = True
        self.no_speaker_adaptation = True
        self.debug = False
        self.errors = True


def align():
    language = 'english'
    corpus_dir = r'D:\Data\Dimensions\truncated'
    output_dir = r'D:\Data\Dimensions\truncated_aligned'
    temp_dir = r'D:\Data\Dimensions\Temp'
    model_path = r'D:\temp\librispeech_models_clean.zip'
    args = DummyArgs()
    #align_included_model(language, corpus_dir, output_dir, temp_dir,
    #                     args)
    align_corpus(model_path, corpus_dir, output_dir, temp_dir,
                         args)

if __name__ == '__main__':
    align()
