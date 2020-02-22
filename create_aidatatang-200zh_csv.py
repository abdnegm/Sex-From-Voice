"""create_aidatatang-200zh_csv.py

Example script on how to create a testing set from the aidatatang-200zh dataset.

This script is mainly intended for demonstration purposes and thus makes a lot of undocumented assumptions.
"""

import csv
import os
import pitchdetect
import re
import soundfile
import sys

def get_identifier(path):
    match = re.search(r"G\d\d\d\d[/\\]T0055G\d\d\d\dS\d\d\d\d.wav$", path)
    return match.group()[:-4] # G\d\d\d\d[/\\]T0055G\d\d\d\dS\d\d\d\d

def get_sex(path, sexes={}):
    if len(sexes) == 0:
        # init sexes
        for root, dirs, files in os.walk(aidatatang_root):
            for filename in files:
                if filename.endswith('.metadata'):
                    with open(os.path.join(root, filename)) as f:
                        lines = f.readlines()
                        for line in lines:
                            line_split = line.split()
                            if line_split[0] == 'SEX':
                                sexes[filename[:-9]] = 0 if line_split[1] == 'Male' else 1

    match = re.search(r"T0055G\d\d\d\dS\d\d\d\d", path)
    return sexes[match.group()]

aidatatang_root = sys.argv[1]
output_fn = sys.argv[2]

audio_roots = []
audio_files = []
for root, dirs, files in os.walk(aidatatang_root):
    for f in files:
        if f.endswith('.wav'):
            audio_roots.append(root)
            audio_files.append(f)

with open(output_fn, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['identifier', 'pitch', 'sex'])
    progress = 0
    for i, filename in enumerate(audio_files):
        if progress % 2400 == 0: # roughly 1%
            print("progress:", progress)
        path = os.path.join(audio_roots[i], filename)
        signal, f_s = soundfile.read(path)
        identifier = get_identifier(path)
        pitch = pitchdetect.fund(signal, f_s)
        sex = get_sex(path)
        csv_writer.writerow([identifier, pitch, sex])
        progress += 1

