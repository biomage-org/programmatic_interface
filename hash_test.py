import hashlib
import json
import re

samples = [
    {
        'metadata': {'Track 2': 'track2', 'Track-4': 'trak4'},
        'name': '10k PBMCs',
        'sampleId': "e175f060-bca8-4f5a-9256-e253ee9de785",
        'type': '10x',
        'options': {},
    }, 
    {
        'options': {},  
        'name': 'WT1',
        'sampleId': "a175f060-bca8-4f5a-9256-e253ee9de785",
        'type': '10x',
        'metadata': {'Track-4': 'track4d', 'Track 2': 'trak2d', },
    }
]

metadata_tracks = ['Track 2', 'Track-4']

sorted_samples = sorted(samples, key = lambda sample: sample['sampleId'])

technology            = samples[0]['type']
sorted_sample_ids     = list(map(lambda sample: sample['sampleId'], sorted_samples))
sorted_sample_options = list(map(lambda sample: sample['options'], sorted_samples))
sorted_sample_names   = list(map(lambda sample: sample['name'], sorted_samples))

data = {
    'organism': None,
    'sampleTechnology': technology,
    'sampleIds': sorted_sample_ids,
    'sampleOptions': sorted_sample_options,
    'sampleNames': sorted_sample_names,
}

if len(metadata_tracks):

    sorted_metadata_tracks = sorted(metadata_tracks) 
    sorted_metadata = {}

    for track in sorted_metadata_tracks:
        sanitized_track = re.sub(r'-+', '_', track)
        sorted_metadata[sanitized_track] = list(map(lambda sample: sample['metadata'][track], sorted_samples))

    data['metadata'] = sorted_metadata

json_data = json.dumps(data, separators=(',', ':')).encode('utf-8')

# print(json_data)



hash = hashlib.sha1()
hash.update(f'string:{len(json_data)}:'.encode('utf-8'))
hash.update(json_data)
res = hash.hexdigest()
print(res)