"""create_sitw_csv.py

Example script on how to create a testing set from the Speakers in the Wild (SITW) dataset.

This script is mainly intended for demonstration purposes and thus makes a lot of undocumented assumptions.
"""

import csv
import os
import pitchdetect
import re
import soundfile
import sys

def get_identifier(path):
    match = re.search(r"(dev|eval)[/\\]audio[/\\][a-z][a-z][a-z][a-z][a-z].flac$", path)
    return match.group()[:-17] + "_" + match.group()[-10:-5] # (dev|eval)_[a-z][a-z][a-z][a-z][a-z]

def get_sex(path, sexes={}):
    if len(sexes) == 0:
        # init sexes
        with open(os.path.join(sitw_root, "dev", "keys", "meta.lst")) as f:
            lines = f.readlines()
            for line in lines:
                line_split = line.split()
                key = line_split[0][6:11]
                sex = 0 if line_split[2] == 'm' else 1
                sexes[key] = sex
        with open(os.path.join(sitw_root, "eval", "keys", "meta.lst")) as f:
            lines = f.readlines()
            for line in lines:
                line_split = line.split()
                key = line_split[0][6:11]
                sex = 0 if line_split[2] == 'm' else 1
                sexes[key] = sex

    match = re.search(r"[a-z][a-z][a-z][a-z][a-z].flac$", path)
    return sexes[match.group()[:5]]

sitw_root = sys.argv[1]
output_fn = sys.argv[2]

audio_roots = []
audio_files = []
for root, dirs, files in os.walk(sitw_root):
    for f in files:
        if f.endswith('.flac'):
            audio_roots.append(root)
            audio_files.append(f)

with open(output_fn, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['identifier', 'pitch', 'sex'])
    progress = 0
    for i, filename in enumerate(audio_files):
        if progress % 50 == 0: # roughly 1%
            print("progress:", progress)
        path = os.path.join(audio_roots[i], filename)
        signal, f_s = soundfile.read(path)
        identifier = get_identifier(path)
        pitch = pitchdetect.fund(signal, f_s)
        sex = get_sex(path)
        csv_writer.writerow([identifier, pitch, sex])
        progress += 1

