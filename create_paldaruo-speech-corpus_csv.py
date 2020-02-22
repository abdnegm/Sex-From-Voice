"""create_paldaruo-speech-corpus_csv.py

Example script on how to create a testing set from the Paldaruo Speech Corpus dataset.

This script is mainly intended for demonstration purposes and thus makes a lot of undocumented assumptions.
"""

import csv
import os
import pitchdetect
import re
import soundfile
import sys

def get_identifier(path):
    match = re.search(r"audio[/\\]wav[/\\][^/\\]*[/\\][^/\\]*.wav$", path)
    return match.group()[10:-4]

def get_sex(path, sexes={}):
    if len(sexes) == 0:
        # init sexes
        with open(os.path.join(paldaruo_root, "metadata.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    sexes[row[0]] = 0 if row[8] == 'gwryw' else 1 # gwryw=male, benyw=female
                line_count += 1

    match = re.search(r"audio[/\\]wav[/\\][^/\\]*[/\\]", path)
    return sexes[match.group()[10:-1]]

paldaruo_root = sys.argv[1]
output_fn = sys.argv[2]

audio_roots = []
audio_files = []
for root, dirs, files in os.walk(paldaruo_root):
    for f in files:
        if f.endswith('.wav'):
            audio_roots.append(root)
            audio_files.append(f)

with open(output_fn, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['identifier', 'pitch', 'sex'])
    progress = 0
    for i, filename in enumerate(audio_files):
        if progress % 140 == 0: # roughly 1%
            print("progress:", progress)
        path = os.path.join(audio_roots[i], filename)
        signal, f_s = soundfile.read(path)
        identifier = get_identifier(path)
        pitch = pitchdetect.fund(signal, f_s)
        sex = get_sex(path)
        csv_writer.writerow([identifier, pitch, sex])
        progress += 1

