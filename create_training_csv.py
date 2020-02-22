"""create_training_csv.py

Example script on how to create the training set from the McGill TSP speech and CMU Arctic datasets.

This script is mainly intended for demonstration purposes and thus makes a lot of undocumented assumptions.
"""

import csv
import os
import pitchdetect
import re
import soundfile
import sys

def get_identifier(path):
    match_mcgill = re.search(r"\d\d?k((-LP7)|(-mIRSS)|(-G712))?[/\\][A-Z][A-Z][/\\][A-Z][A-Z]\d\d_\d\d.wav$", path)
    if match_mcgill:
        return match_mcgill.group()[:-15] + "_" + match_mcgill.group()[-11:-4] # \d\d?k((-LP7)|(-mIRSS)|(-G712))?_[A-Z][A-Z]\d\d_\d\d

    match_cmu = re.search(r"cmu_[a-z][a-z]_[a-z][a-z][a-z]_arctic[/\\]wav[/\\]arctic_[ab]\d\d\d\d.wav$", path)
    if match_cmu:
        return match_cmu.group()[:17] + match_cmu.group()[28:34] # cmu_[a-z][a-z]_[a-z][a-z][a-z]_arctic_[ab]\d\d\d\d

    raise Exception("Cannot determine the identifier.")

def get_sex(path):
    match_mcgill = re.search(r"[A-Z][A-Z]\d\d_\d\d\.wav$", path)
    if match_mcgill:
        start = match_mcgill.span()[0]
        return 0 if path[start] == 'M' else 1

    match_cmu = re.search(r"cmu_[a-z][a-z]_[a-z][a-z][a-z]_arctic", path)
    if match_cmu:
        start = match_cmu.span()[0]
        return 1 if path[start+7:start+10] == 'clb' or path[start+7:start+10] == 'slt' else 0

    raise Exception("Cannot determine the sex.")

training_root = sys.argv[1]
output_fn = sys.argv[2]

audio_roots = []
audio_files = []
for root, dirs, files in os.walk(training_root):
    for f in files:
        if f.endswith('.wav'):
            audio_roots.append(root)
            audio_files.append(f)

with open(output_fn, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['identifier', 'pitch', 'sex'])
    for i, filename in enumerate(audio_files):
        path = os.path.join(audio_roots[i], filename)
        print("path:", path)
        signal, f_s = soundfile.read(path)
        identifier = get_identifier(path)
        pitch = pitchdetect.fund(signal, f_s)
        sex = get_sex(path)
        csv_writer.writerow([identifier, pitch, sex])

