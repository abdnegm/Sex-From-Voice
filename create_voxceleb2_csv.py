"""create_voxceleb2_csv.py

Example script on how to create a testing set from the VoxCeleb2 dataset.

This script is mainly intended for demonstration purposes and thus makes a lot of undocumented assumptions.
"""

import csv
import os
import pitchdetect
import re
from pydub import AudioSegment
import sys

def get_identifier(path):
    match = re.search(r"id\d\d\d\d\d[/\\][^/\\]*[/\\]\d\d\d\d\d.m4a$", path)
    return match.group()[:-4] # id\d\d\d\d\d[/\\][^/\\]*[/\\]\d\d\d\d\d

def get_sex(path, sexes={}):
    if len(sexes) == 0:
        # init sexes
        with open(os.path.join(voxceleb2_root, "vox2_meta.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    sexes[row[0]] = 0 if row[2] == 'm' else 1
                line_count += 1

    match = re.search(r"id\d\d\d\d\d", path)
    return sexes[match.group()]

voxceleb2_root = sys.argv[1]
output_fn = sys.argv[2]

audio_roots = []
audio_files = []
for root, dirs, files in os.walk(voxceleb2_root):
    for f in files:
        if f.endswith('.m4a'):
            audio_roots.append(root)
            audio_files.append(f)

with open(output_fn, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['identifier', 'pitch', 'sex'])
    progress = 0
    for i, filename in enumerate(audio_files):
        if progress % 1000 == 0: # roughly 0.1%
            print("progress:", progress)
        path = os.path.join(audio_roots[i], filename)
        sound = AudioSegment.from_file(path, format='m4a')
        signal = sound.get_array_of_samples()
        f_s = sound.frame_rate
        identifier = get_identifier(path)
        pitch = pitchdetect.fund(signal, f_s)
        sex = get_sex(path)
        csv_writer.writerow([identifier, pitch, sex])
        progress += 1

