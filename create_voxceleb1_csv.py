"""create_voxceleb1_csv.py

Example script on how to create a testing set from the VoxCeleb1 dataset.

This script is mainly intended for demonstration purposes and thus makes a lot of undocumented assumptions.
"""

import csv
import os
import pitchdetect
import re
import soundfile
import sys

def get_identifier(path):
    match_dev = re.search(r"vox1_dev_wav[/\\]wav[/\\]id\d\d\d\d\d[/\\][^/\\]*[/\\]\d\d\d\d\d.wav$", path)
    if match_dev:
        return match_dev.group()[5:9] + match_dev.group()[17:-4] # dev_id\d\d\d\d\d[/\\][^/\\]*[/\\]\d\d\d\d\d
    match_test = re.search(r"vox1_test_wav[/\\]wav[/\\]id\d\d\d\d\d[/\\][^/\\]*[/\\]\d\d\d\d\d.wav$", path)
    if match_test:
        return match_test.group()[5:10] + match_test.group()[18:-4] # test_id\d\d\d\d\d[/\\][^/\\]*[/\\]\d\d\d\d\d

def get_sex(path, sexes={}):
    if len(sexes) == 0:
        # init sexes
        with open(os.path.join(voxceleb1_root, "vox1_meta.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    sexes[row[0]] = 0 if row[2] == 'm' else 1
                line_count += 1

    match = re.search(r"id\d\d\d\d\d", path)
    return sexes[match.group()]

voxceleb1_root = sys.argv[1]
output_fn = sys.argv[2]

audio_roots = []
audio_files = []
for root, dirs, files in os.walk(voxceleb1_root):
    for f in files:
        if f.endswith('.wav'):
            audio_roots.append(root)
            audio_files.append(f)

with open(output_fn, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['identifier', 'pitch', 'sex'])
    progress = 0
    for i, filename in enumerate(audio_files):
        if progress % 1500 == 0: # roughly 1%
            print("progress:", progress)
        path = os.path.join(audio_roots[i], filename)
        signal, f_s = soundfile.read(path)
        identifier = get_identifier(path)
        pitch = pitchdetect.fund(signal, f_s)
        sex = get_sex(path)
        csv_writer.writerow([identifier, pitch, sex])
        progress += 1

