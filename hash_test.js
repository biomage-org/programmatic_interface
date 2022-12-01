const objectHash = require('object-hash');

const METADATA_DEFAULT_VALUE = 'N.A.';

const samples = [
    {
        'name': '10k PBMCs',
        'sampleId': "e175f060-bca8-4f5a-9256-e253ee9de785",
        'type': '10x',
        'options': {},
        'metadata': {'Track-4': 'trak4', 'Track 2': 'track2'},
    }, 
    {
        'name': 'WT1',
        'sampleId': "a175f060-bca8-4f5a-9256-e253ee9de785",
        'type': '10x',
        'metadata': {'Track 2': 'trak2d', 'Track-4': 'track4d'},
        'options': {},    
    }
]

const metadataTracks = ['Track-4', 'Track 2']

const sortedSamples = samples.sort((sample1, sample2) => { 
    id1 = sample1.sampleId;
    id2 = sample2.sampleId;

    if (id1 > id2) return 1;
    if (id1 < id2) return -1;
    return 0;
});

const technology = sortedSamples[0].type;
const sortedSampleIds = sortedSamples.map(sample => sample.sampleId);
const sortedOptions = sortedSamples.map(sample => sample.options); 
const sortedNames = sortedSamples.map(sample => sample.name);

const data = {
    'organism': null,
    'sampleTechnology': technology,
    'sampleIds': sortedSampleIds,
    'sampleOptions': sortedOptions,
    'sampleNames': sortedNames,
}

if (metadataTracks.length) {
    const sortedMetadataTracks = metadataTracks.sort();

    const sortedMetadata = sortedMetadataTracks.reduce((acc, track) => {
        metadataBySample = sortedSamples.map(sample => sample.metadata[track] || METADATA_DEFAULT_VALUE);
        // Make sure the key does not contain '-' as it will cause failure in GEM2S
        sanitizedTrack = track.replace(/-+/g, '_');
        return {...acc,  [sanitizedTrack]: metadataBySample };
    }, {});

    data.metadata = sortedMetadata;
}

const string_data = JSON.stringify(data)
console.log(objectHash.sha1(string_data));