

import os
import sys
import shutil

orig_data_dirs = [r'C:\Users\michael\Dropbox\dimensions\2_suborn\2_data\1_soundfiles',
                    r'C:\Users\michael\Dropbox\dimensions\2_suborq\2_data\1_soundfiles']
orig_data_dirs = [r'C:\Users\michael\Dropbox\dimensions\2_suborn\3_truncate\truncated',
                    r'C:\Users\michael\Dropbox\dimensions\2_suborq\3_truncate\truncated']

working_dir = r'D:\Data\Dimensions\original_dimensions'
working_dir = r'D:\Data\Dimensions\truncated'
aligned_directory = r'D:\Data\Dimensions\truncated_aligned'

skip_speakers = ['suborq_1251', 'suborn_1251', 'suborq_1252', 'suborn_1252']

def collect_originals():
    for d in orig_data_dirs:
        for f in os.listdir(d):
            if not f.endswith('.wav'):
                continue
            name, _ = os.path.splitext(f)
            speaker_name = '_'.join(name.split('_')[:-2])
            if speaker_name in skip_speakers:
                continue
            lab_file = name + '.lab'
            out_dir = os.path.join(working_dir, speaker_name)
            os.makedirs(out_dir, exist_ok = True)
            out_path = os.path.join(out_dir, f)
            out_lab_path = os.path.join(out_dir, lab_file)
            shutil.copyfile(os.path.join(d, f), out_path)
            shutil.copyfile(os.path.join(d, lab_file), out_lab_path)

def add_wavs():
    speakers = os.listdir(aligned_directory)
    for s in speakers:
        speaker_dir = os.path.join(aligned_directory, s)
        if not os.path.isdir(speaker_dir):
            continue
        for f in os.listdir(speaker_dir):
            if not f.endswith('.TextGrid'):
                continue
            name, _ = os.path.splitext(f)
            wav = os.path.join(working_dir, s, name + '.wav')
            out_path = os.path.join(speaker_dir, name + '.wav')
            if not os.path.exists(out_path):
                shutil.copyfile(wav, out_path)

if __name__ == '__main__':
    #collect_originals()
    add_wavs()
