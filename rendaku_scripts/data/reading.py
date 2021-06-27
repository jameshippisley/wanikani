class Reading():
    def __init__(self, kanji, kana, type, base_reading=None, is_rendaku=False, is_tsu=False):
        self.kanji = kanji
        self.kana = kana
        self.type = type
        self.base_reading = base_reading
        self.is_rendaku = is_rendaku
        self.is_tsu = is_tsu

    @property
    def character(self):
        if self.kanji:
            return self.kanji.character
        else:
            return self.kana

    def all_readings(self, first=None, last=None, prior=None):
        katakana = ('アイウエオ'
                    'カキクケコ'
                    'ガギグゲゴ'
                    'マミムメモ'
                    'タチツテト'
                    'サシスセソ'
                    'ザジズゼゾ'
                    'ラリルレロ'
                    'ハヒフヘホ'
                    'バビブベボ'
                    'パピプペポ'
                    'ナニヌネノ'
                    'ン'
                    'ッェャ'
                    )
        hiragana = ('あいうえお'
                    'かきくけこ'
                    'がぎぐげご'
                    'まみむめも'
                    'たちつてと'
                    'さしすせそ'
                    'ざじずぜぞ'
                    'らりるれる'
                    'はひふへほ'
                    'ばびぶべぼ'
                    'ぱぴぷぺぽ'
                    'なにぬねの'
                    'ん'
                    'っぇゃ'
                    )
        pos = katakana.find(self.kana)
        if pos >= 0:
            return [self, Reading(None, hiragana[pos], 'kana')]
        else:
            return [self]

    def rendaku_readings(self):
        rendaku_chars = {
            'か': ['が'],
            'き': ['ぎ'],
            'く': ['ぐ'],
            'け': ['	げ'],
            'こ': ['ご'],
            'さ': ['ざ'],
            'し': ['じ'],
            'す': ['ず'],
            'せ': ['ぜ'],
            'そ': ['ぞ'],
            'た': ['だ'],
            'ち': ['ぢ'],
            'つ': ['づ'],
            'て': ['で'],
            'と': ['ど'],
            'は': ['ば', 'ぱ'],
            'ひ': ['び', 'ぴ'],
            'ふ': ['ぶ', 'ぷ'],
            'へ': ['べ', 'ぺ'],
            'ほ': ['ぼ', 'ぽ'],
            # 'ぼ': ['ぽ'],
            # 'ば': ['ぱ'],
            # 'び': ['ぴ'],
            # 'ぶ': ['ぷ'],
            # 'べ': ['ぺ'],
            # 'ぼ': ['ぽ'],
        }.get(self.kana[0], [])

        rendaku_readings = []
        for char in rendaku_chars:
            new_kana = char + self.kana[1:]
            new_reading = Reading(
                kanji=self.kanji,
                kana=new_kana,
                type=self.type,
                base_reading=self,
                is_rendaku=True,
                is_tsu=self.is_tsu)
            rendaku_readings.append(new_reading)

        return rendaku_readings

    def tsu_readings(self):
        tsu_chars = ['っ']

        tsu_readings = []
        for char in tsu_chars:
            new_kana = self.kana[:-1] + char
            new_reading = Reading(
                kanji=self.kanji,
                kana=new_kana,
                type=self.type,
                base_reading=self,
                is_rendaku=self.is_rendaku,
                is_tsu=True)
            tsu_readings.append(new_reading)

        return tsu_readings

    def has_voiced_obstruent(self):
        thing = self.base_reading or self

        if thing.contains(
            'が', 'ぎ', 'ぐ', 'げ', 'ご',
            'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
            'だ', 'ぢ', 'づ', 'で', 'ど',
            'ば', 'び', 'ぶ', 'べ', 'ぼ',
            'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ',
            'が', 'ギ', 'グ', 'ゲ', 'ゴ',
            'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
            'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
            'バ', 'ビ', 'ブ', 'ベ', 'ボ',
            'パ', 'ピ', 'プ', 'ペ', 'ポ',
        ):
            return True

        return False

    def contains(self, *chars):
        for char in chars:
            if char in self.kana:
                return True
        return False

    def ends_with(self, *strings):
        for string in strings:
            if self.kana.endswith(string):
                return True
        return False

    def starts_with(self, *strings):
        for string in strings:
            if self.kana.startswith(string):
                return True
        return False
