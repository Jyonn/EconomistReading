import json
import os
import string

from tqdm import tqdm

path = 'words'
files = os.listdir(path)

word_depot = dict()
pos = set()
types = set()

for file in tqdm(files):
    words = json.load(open(os.path.join(path, file), 'r'))
    for word in tqdm(words):
        if ' ' in word:
            continue

        partOfSpeeches = []
        for r_partOfSpeech in words[word]['ds']:
            r_partOfSpeech['s'] = r_partOfSpeech['s'].replace('.', '')
            if r_partOfSpeech['s'].startswith('nou'):
                r_partOfSpeech['s'] = 'noun'
            if r_partOfSpeech['s'].startswith('ver'):
                r_partOfSpeech['s'] = 'verb'

            pos.add(r_partOfSpeech['s'])

            partOfSpeech = dict(
                partOfSpeech=r_partOfSpeech['s'],
                definitions=[],
            )

            for r_definition in r_partOfSpeech['ms']:
                definition = dict(
                    definition=r_definition['m'],
                    collocations=[],
                )

                for r_collocation in r_definition['cs']:
                    if r_collocation['s'] == 'VERB + ' + word.upper():
                        r_collocation['s'] = 'V+'
                    if r_collocation['s'] == word.upper() + ' + VERB':
                        r_collocation['s'] = '+V'
                    if r_collocation['s'] == 'NOUN + ' + word.upper():
                        r_collocation['s'] = 'N+'
                    if r_collocation['s'] == word.upper() + ' + NOUN':
                        r_collocation['s'] = '+N'
                    types.add(r_collocation['s'])

                    collocation = dict(
                        type=r_collocation['s'],
                        instances=[]
                    )

                    for r_instance in r_collocation['ps']:
                        if r_instance[0].startswith('| '):
                            r_instance[0] = r_instance[0][2:]
                        instance = dict(
                            vocabs=r_instance[0],
                            sentences=[]
                        )

                        for r_sentence in r_instance[1]:
                            if r_sentence[0] in string.ascii_uppercase and r_sentence[-1] not in '.?':
                                r_sentence += '.'
                            instance['sentences'].append(r_sentence)

                        collocation['instances'].append(instance)

                    definition['collocations'].append(collocation)

                partOfSpeech['definitions'].append(definition)

            partOfSpeeches.append(partOfSpeech)

        word_depot[word] = partOfSpeeches


json.dump(word_depot, open('word-depot.json', 'w'))

print(pos)
print(types)
