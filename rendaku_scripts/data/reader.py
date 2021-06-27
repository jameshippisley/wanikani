import data.vocab
import data.kanji

import os
this_dir = os.path.dirname(os.path.realpath(__file__))

vocab_file = os.path.join(this_dir, 'vocab.txt')
kanji_file = os.path.join(this_dir, 'kanji.txt')
custom_kanji_file = os.path.join(this_dir, 'custom_kanji.txt')

def get_all_vocab():
    items = read_file(vocab_file)

    kanji_dict = get_kanji_dict()

    vocab_list = []
    for item in items:
        word = data.vocab.Vocab(
            string=item['character'],
            meanings=split_and_strip(item['meaning']),
            readings=split_and_strip(item['kana']),
            level=item['level'],
            kanji_dict=kanji_dict,
        )

        vocab_list.append(word)

    return vocab_list


def get_all_kanji():
    items = read_file(kanji_file)
    custom_items = read_file(custom_kanji_file)

    kanji_list = []
    for item in items:
        onyomi_readings = split_and_strip(item['onyomi'], ignore_none=True)
        kunyomi_readings = split_and_strip(item['kunyomi'], ignore_none=True)

        for custom_item in custom_items:
            if custom_item['character'] == item['character']:
                onyomi_readings += split_and_strip(custom_item['onyomi'], ignore_none=True)
                kunyomi_readings += split_and_strip(custom_item['kunyomi'], ignore_none=True)

        kanji = data.kanji.Kanji(
            character=item['character'],
            meanings=split_and_strip(item['meaning']),
            onyomi_readings=onyomi_readings,
            kunyomi_readings=kunyomi_readings,
            level=item['level'])

        kanji_list.append(kanji)

    return kanji_list

def split_and_strip(text,ignore_none=False):
    if ignore_none and text == 'None':
        return []

    return [x.strip() for x in text.split(',') if x.strip()]

def get_kanji_dict():
    kanji_dict = {}
    for kanji in get_all_kanji():
        kanji_dict[kanji.character] = kanji
    return kanji_dict


def read_file(filename):
    data = []
    with open(filename, 'rU') as f:
        for line in f:
            words = line.strip().split(';')
            if words[0] == '#key':
                keys = words
            elif words[0] and words[0][0] == '#':
                pass  # a comment
            else:
                if len(words) != len(keys):
                    raise ValueError(f"keys ({len(keys)}) do not match line ({len(words)}):\n words: {words}\n keys:  {keys}\n")
                item = {}
                for i in range(0,len(keys)):
                    item[keys[i]] = words[i]
                data.append(item)
    return data




