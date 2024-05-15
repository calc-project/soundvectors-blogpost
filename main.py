from collections import defaultdict
from pyclts import CLTS
from soundvectors import SoundVectors
from tabulate import tabulate


clts = CLTS()
sv = SoundVectors(ts=clts.bipa)


def load_data(id):
    transcriptiondata = clts.transcriptiondata(id)
    unique_sounds = set(transcriptiondata.sounds)
    unique_sounds.remove("<NA>")
    return unique_sounds, transcriptiondata.data


def map_vector_to_sounds(sounds, vector_func):
    features_to_sound = defaultdict(list)
    for s in sounds:
        features_to_sound[vector_func(s)].append(s)

    return features_to_sound, len(features_to_sound), len(sounds)


if __name__ == "__main__":
    table = []
    for system in ["phoible", "panphon"]:
        unique_sounds, data = load_data(system)
        _, num_unique_vecs_own, num_unique_sounds = map_vector_to_sounds(unique_sounds, lambda x: data[x][0]["features"])
        _, num_unique_soundvecs, _ = map_vector_to_sounds(unique_sounds, sv.get_vec)
        table.append([system.upper(), num_unique_sounds, num_unique_vecs_own, num_unique_soundvecs])

    print(tabulate(table, headers=["SOURCE", "UNIQUE SOUNDS", "UNIQUE VECTORS (OWN)", "UNIQUE VECTORS (SOUNDVEC)"]))
