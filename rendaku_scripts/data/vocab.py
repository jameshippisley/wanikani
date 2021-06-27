import data.reading

# Ideas:
#   - Check message for word "profound"
#   - Analyse the small tsu
#   - Transitive vs intransitive (verb comparison) section?
#   - Add more extra irregular readings for kanji so we can analyse rendaku on irregular cases
#   - Look for more patterns/explanations in the current exceptions
#      - Place names
#      - xxx AND yyy type meaning

class Vocab():
    def __init__(self, string, meanings, readings, level, kanji_dict):
        self.string = string  # String of characters (kanji + kana) making up vocab
        self.meanings = meanings  # List of english meanings
        self.readings = readings  # List of allowed kana readings
        self.level = level  # Wanikani level

        self.interpreted_readings = self.get_interpreted_readings(kanji_dict)

        self.irregular_readings = self.get_irregular_readings(self.interpreted_readings)

        #print(self.get_summary())

    def get_interpreted_readings(self, kanji_dict):

        possible_readings = [[]]

        prior = None
        for pos in range(len(self.string)):
            character = self.string[pos]
            if character == '〜':
                continue
            first = pos == 0
            last = pos == len(self.string) - 1
            new_possible_readings = []
            kanji = kanji_dict.get(character)
            if kanji is None:
                kanji = data.reading.Reading(
                    kanji = None,
                    kana = character,
                    type = 'kana',
                )
            for reading in possible_readings:
                for kanji_reading in kanji.all_readings(first, last, prior):
                    new_possible_readings.append(reading + [kanji_reading])

            possible_readings = new_possible_readings

            prior = kanji

        readings = []
        for reading in possible_readings:
            kana = ''
            for character in reading:
                try:
                    kana += character.kana
                except AttributeError:
                    kana += character
            if kana in self.readings:
                readings.append(reading)

        return readings

    def get_irregular_readings(self, interpreted_readings):
        regular_reading_list = []
        for reading in interpreted_readings:
            kana = ''
            for character in reading:
                kana += character.kana

            regular_reading_list += [kana]

        return [x for x in self.readings if not (x in regular_reading_list)]

    def analyze_rendaku(self):
        rendakus_list = []

        for reading in self.interpreted_readings:
            kana = ''
            kanji = ''
            for character in reading:
                kana += character.kana
                kanji += character.character

            rendakus = []
            for pos, character in enumerate(reading):

                # No rendaku on first character
                if pos==0:
                    continue

                # No rendaku on kana
                if character.type == 'kana':
                    continue

                # No rendaku if this character can't rendaku
                if not (character.is_rendaku or len(character.rendaku_readings())):
                    continue

                (should_rendaku, why) = self.predict_rendaku(reading, kanji, pos)

                rendakus.append([should_rendaku, why, pos])

            for rendaku in rendakus:
                (should_rendaku, why, pos) = rendaku

                if isinstance(should_rendaku, str):
                    end = reading[pos-1].kana + reading[pos].kana[0]
                    got_it_right = end.endswith(should_rendaku)
                    if got_it_right:
                        message = f"does change to {should_rendaku} because {why}"
                    else:
                        message = f"does not change to {should_rendaku} even though {why}"
                elif should_rendaku:
                    got_it_right = bool(reading[pos].is_rendaku)
                    if got_it_right:
                        message = f"does rendaku because {why}"
                    else:
                        message = f"does not rendaku. You might think it should rendaku because {why}"
                else:
                    got_it_right = not bool(reading[pos].is_rendaku)
                    if got_it_right:
                        message = f"does not rendaku because {why}"
                    else:
                        message = f"does rendaku. You might think it should not rendaku because {why}"

                rendakus_list.append({
                    'word': self,
                    'reading': reading,
                    'kana': kana,
                    'kanji': kanji,
                    'pos': pos,
                    'should_rendaku': should_rendaku,
                    'got_it_right': got_it_right,
                    'message': message})

        return rendakus_list

    def predict_rendaku(self, reading, kanji, pos):
        this = reading[pos].base_reading or reading[pos]
        before = reading[pos - 1].base_reading or reading[pos - 1]

        it = f"{this.character}({this.kana})"

        if this.starts_with('は', 'ひ', 'ふ', 'へ', 'ほ'):
            p_kana = 'ぱぴぷぺぽ'['はひふへほ'.index(this.kana[0])]
            if before.ends_with('ん','っ'):
                return (p_kana, f"h almost always changes to p after {before.kana[-1]}")

            if before.kana in ['いち', 'にち']:
                becomes = f"{before.kana[0]}っ{p_kana}"
                return (becomes, f"{before.kana} followed by h always changes to {before.kana[0]}っ followed by p")

            if before.ends_with('つ') and len(before.kana) > 1:
                becomes = f"っ{p_kana}"
                return (becomes, f"~つ followed by h almost always changes to ~っ followed by p")

        possible_rendaku = this.rendaku_readings()[0].kana
        if possible_rendaku in [x.kana for x in this.kanji.all_readings()]:
            return (True,
                    f"{possible_rendaku} and {this.kana} are valid readings for {this.character} (in which case the rendaku'd one is almost always chosen)")

        if '白' in kanji or '黒' in kanji:
            if kanji in ['白菊', '黒板']:
                return (True, f"there are only two words in wanikani containing either black (黒) or white (白) "
                              f"which rendaku (黒板 - \"blackboard\" and 白菊 - \"white chrystanthemum\") and this is one of them")
            else:
                return (False, f"there only two words in wanikani containing either black (黒) or white (白) "
                              f"which rendaku (黒板 - \"blackboard\" and 白菊 - \"white chrystanthemum\") and this is not one of them")

        if this.type == 'onyomi':

            if this.character in [
                '版',  # "edition (はん)"
                '板',  # "board (はん)"
            ]:
                if kanji == '初版':
                    return (False, f"\"First Edition\" is an exception to an exception. "
                                   f"You might think it would rendaku because {it} is one of two visually "
                                   f"similar はん kanji (版 - edition and 板 - board) "
                                   f"which rendaku for all other words in wanikani despite being onyomi")
                else:
                    return (True, f"{it} is one of two visually similar はん kanji (版 - edition and 板 - board) "
                                  f"which almost always rendaku in wanikani despite being onyomi. "
                                  f"(The only exception to this exception is 初版(しょはん) - \"First Edition\")")


            if before.character + this.character in [
                '誕生',  # "birth"
                '経済',  # "economics"
            ]:
                return (True, f"{before.character}{this.character} is a word that always does rendaku, even though {it} is onyomi")

            if before.character + this.character in [
                '面倒',  # "trouble"
            ]:
                return (True, f"although {it} is onyomi and therefore should not rendaku, this word is trouble. Rendaku Trouble. \"Mendoza!\" as the Simpson's McBain would say")

            if this.character == '国':
                if before.character + this.character in [
                '中国',  # China
                '天国',  # Heaven
                '隣国',  # Neighboring country
                ]:
                    return (True,
                            f"although {it} is onyomi, {before.character}{this.character} is one of the three countries in WaniKani (China, Heaven and the Neighboring Country) that you really want to go (ご!) to")
                else:
                    return (False, f"{it} is onyomi and {before.character}{this.character} is not one of the three countries in WaniKani (China, Heaven and the Neighboring Country) that rendaku inspite of being onyomi")


            if kanji in [
                '足し算',  # "Addition"
                '引き算',  # "Subtraction"
                '掛け算',  # "Multiplication"
                '割り算',  # "Division"
                '珠算',  # "Calculation with an abacus"
            ]:
                return (True, f"although {it} is onyomi, {kanji} is one of the five types of calculation in WaniKani (addition, subtraction, multiplication, division and calculating with an abacus) that rendaku")

            if kanji in [
                '近所',  # Neighborhood
                '便所',  # Toilet,
                '休憩所',  # Rest stop,
                '給油所',  # Gas station
            ] and reading[pos].kana == 'じょ':
                return (True, f"although {it} is onyomi, {kanji} is one of the four places in WaniKani (your friendly neighborhood/toilet/rest area/gas station) where {it} rendakus")

            return(False, f"{it} is onyomi, and none of the exceptional circumstances which cause onyomi readings to rendaku apply")

        if this.has_voiced_obstruent():
            return (False, f"{it} already has dakuten (Lyman's Law)")

        for i in range(pos+1,len(reading)):
            next = reading[i].base_reading or reading[i]
            if next.has_voiced_obstruent():
                return (False, f"a subsequent character ({next.kana}) already has dakuten (Lyman's law)")

# 50/50...
#        if this.kana[0] == 'つ':
#            return (False, f"{this.kana[0]} usually does not rendaku")

        # make's it worse for now
#        if reading[pos-1].type == 'onyomi':
#            return (False, f"prior reading ({reading[pos-1].kanji}/{reading[pos-1].kana}) is onyomi")

        if before.kana == 'お':
            return (False, f"the prior character is an honorific prefix")

        if before.kana in ['の', 'を', 'が']:
            return (False, f"the prior character ({before.kana}) is a particle")

        if this.character in "様込手付死方返先差鹿崎":
            return (False, f"rendaku almost never occures on {it} (even though it is konyomi)")

        if this.character == '日' and [x for x in self.meanings if x.endswith('days')]:
            return (False, f"~{this.character} (days counter) does not rendaku")

        if this.character == '島':
            if kanji in ['田代島', '軍艦島']:
                return (True, f"{kanji} is one of the two islands in WaniKani (Tashirojima and Gunkanjima) where the {it} reading does rendaku")
            else:
                return (False, f"even though {it} is kunyomi, it does not usually rendaku (the only exceptions in WaniKani are Tashirojima and Gunkanjima)")

        if kanji == '面倒臭い':
             return (False, f"although {it} is kunyomi and therefore should rendaku, this word is trouble. Rendaku Trouble. \"Mendoza!\" as the Simpson's McBain would say")

        return (True, f"{it} is kunyomi, and none of the exceptional circumstances which stop kunyomi readings from rendaku'ing apply")

    def get_summary(self):
        string = ''
        string += f"{self.string} ("
        string += ", ".join(self.readings)
        string += ")\n"

        for reading in self.interpreted_readings:
            string += "  "
            for character in reading:
                string += character.kana
                string += " "
            string += "\n"

        return string





