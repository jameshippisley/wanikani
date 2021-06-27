import data

def ja(text):
#    return text
    return '<span lang="ja">' + text + "</span>"

rendaku_info = {}
for word in data.get_all_vocab():
    info = {}

    rendakus = word.analyze_rendaku()
    rendakus.sort(key=lambda x: x['pos'])

    for rendaku in rendakus:
        pos = rendaku['pos']
        message = rendaku['message']
        kana = rendaku['kana']
        got_it_right = rendaku['got_it_right']

        annotated_kanji = ''
        annotated_kana = ''
        for i, character in enumerate(rendaku['reading']):
            if i == pos:
                annotated_kana += '<span style="background-color:#ffd6f1;">'
                annotated_kanji += '<span style="background-color:#ffd6f1;">'

            annotated_kana += character.kana
            annotated_kanji += character.character
            if i == pos:
                annotated_kana += '</span>'
                annotated_kanji += '</span>'

        annotated_kanji_ja = ja(annotated_kanji)
        annotated_kana_ja = ja(annotated_kana)

        if not got_it_right:
            message = '<span <span style="background-color:#fdff32;">unexpectedly</span> ' + message

        full_message = f"{annotated_kanji_ja} ({annotated_kana_ja}) {message}.<br>\n"

        old_info = info.get(kana,'')
        if not full_message in old_info:
            info[kana] = old_info + full_message

    for reading in word.interpreted_readings:
        kana = ''
        kanji = ''
        for character in reading:
            kana += character.kana
            kanji += character.character

        if not info.get(kana):
            kanji_ja = ja(kanji)
            kana_ja = ja(kana)
            info[kana] = f"{kanji_ja} ({kana_ja}) has no possible rendaku.<br>\n"

    html = ''
    for reading in word.readings:
        if info.get(reading):
            html += info[reading]
        else:
            kanji_ja = ja(word.string)
            kana_ja = ja(reading)
            html += f"{kanji_ja} ({kana_ja}) is an irregular reading so it is not considered by the rendaku script.<br>\n"

    rendaku_info[word.string] = html

import json
print('DATA = ' + json.dumps(rendaku_info, separators=(',',':')))











