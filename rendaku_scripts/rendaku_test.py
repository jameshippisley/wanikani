import data

all_rendakus = []
for word in data.get_all_vocab():
#    for reading in word.irregular_readings:
#        print(f"{word.string}({reading}) is irregular")

    for rendaku in word.analyze_rendaku():
        all_rendakus.append(rendaku)

frequency = {}
for rendaku in all_rendakus:
    key = rendaku['kanji'][rendaku['pos']] + rendaku['message']
    frequency[key] = frequency.get(key, 0) + 1

all_rendakus.sort(key=lambda x: x['kanji'])
all_rendakus.sort(key=lambda x: x['kanji'][x['pos']])
all_rendakus.sort(key=lambda x: -frequency[x['kanji'][x['pos']] + x['message']])
all_rendakus.sort(key=lambda x: x['message'])

max_kanji_width = max([len(x['kanji']) for x in all_rendakus])
max_kana_width = max([len(x['kana']) for x in all_rendakus])

for rendaku in all_rendakus:
    if rendaku['got_it_right']:
        continue

    pos = rendaku['pos']
    kanji = (rendaku['kanji'][:pos] + ' ' + rendaku['kanji'][pos:]).ljust(max_kanji_width+1, '\u3000')
    kana = rendaku['kana'].ljust(max_kana_width, '\u3000')
    message = rendaku['message']
    meanings = rendaku['word'].meanings

    print(f"{kanji} {kana} {message} (", end='')
    print(", ".join([x.capitalize() for x in meanings]), end='')
    print(").")

total = 0
correct = 0
wrong_should_rendaku = 0
wrong_shouldnt_rendaku = 0

for rendaku in all_rendakus:
    total += 1
    if rendaku['got_it_right']:
        correct += 1
    elif rendaku['should_rendaku']:
        wrong_should_rendaku += 1
    else:
        wrong_shouldnt_rendaku += 1

print(f"Correct: {correct} ({100.0 * correct/total:.1f} %)")
print(f"Wrong:   {total - correct} ({100.0 * (total-correct) / total:.1f} %)")
print(f"Wrong (really does): {wrong_shouldnt_rendaku} ({100.0 * wrong_shouldnt_rendaku / total:.1f} %)")
print(f"Wrong (really wont): {wrong_should_rendaku} ({100.0 * wrong_should_rendaku / total:.1f} %)")
print(f"Total:   {total}")








