import hashlib
import json
import re

samples = [{'metadata': {'wow': 'amazing'}, 'name': 'WT1', 'sampleId': '195b8930-2750-431c-bac7-0fa334c1c6c1', 'type': '10x', 'options': {}}, {'metadata': {'wow': 'N.A.'}, 'name': '10k PBMCs', 'sampleId': '9c1cca61-78ed-4314-a215-f7d6c21c08f5', 'type': '10x', 'options': {}}]

metadata_tracks = ['wow']

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

print(json_data)

hash = hashlib.sha1()

prefix = 'object:9:string:9:prototype:Undefined,string:9:__proto__:object:3:string:9:prototype:Undefined,string:9:__proto__:Null,string:11:constructor:fn:string:8:[native]string:20:function-name:Objectobject:0:,,string:11:constructor:fn:string:8:[native]string:20:function-name:Objectstring:12:[CIRCULAR:2],string:8:metadata:object:4:string:9:prototype:Undefined,string:9:__proto__:string:12:[CIRCULAR:1],string:11:constructor:fn:string:8:[native]string:20:function-name:Objectstring:12:[CIRCULAR:2],string:3:wow:array:2:string:7:amazingstring:4:N.A.,,string:8:organism:Null,string:9:sampleIds:array:2:string:36:195b8930-2750-431c-bac7-0fa334c1c6c1string:36:9c1cca61-78ed-4314-a215-f7d6c21c08f5,string:11:sampleNames:array:2:string:3:WT1string:9:10k PBMCs,string:13:sampleOptions:array:2:object:3:string:9:prototype:Undefined,string:9:__proto__:string:12:[CIRCULAR:1],string:11:constructor:fn:string:8:[native]string:20:function-name:Objectstring:12:[CIRCULAR:2],object:3:string:9:prototype:Undefined,string:9:__proto__:string:12:[CIRCULAR:1],string:11:constructor:fn:string:8:[native]string:20:function-name:Objectstring:12:[CIRCULAR:2],,string:16:sampleTechnology:string:3:10x,'
hash.update(prefix.encode('utf-8'))
# hash.update(json_data)
res = hash.hexdigest()
print(res)


#330c29488de122d024821814ccfafb1d9c505c30