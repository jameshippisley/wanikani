import data.reading

class Kanji():
    def __init__(self, character, meanings, onyomi_readings, kunyomi_readings, level):
        self.character = character
        self.meanings = meanings
        self.onyomi_readings = onyomi_readings
        self.kunyomi_readings = kunyomi_readings
        self.level = level

        self._all_readings = self.get_interpreted_readings()

    def get_interpreted_readings(self):
        all_readings = []

        for reading in self.onyomi_readings:
            all_readings.append(data.reading.Reading(
                kanji=self,
                kana=reading,
                type='onyomi'))

        for reading in self.kunyomi_readings:
            all_readings.append(data.reading.Reading(
                kanji=self,
                kana=reading,
                type='kunyomi'))

        return all_readings

    def all_readings(self, first=True, last=True, prior=None):
        readings = self._all_readings

        if not first:
            new_readings = readings + []
            for reading in readings:
                assert (not reading.is_rendaku)
                for rendaku_reading in reading.rendaku_readings():
                    new_readings.append(rendaku_reading)
            readings = new_readings

        if not last:
            new_readings = readings + []
            for reading in readings:
                assert (not reading.is_tsu)
                for tsu_reading in reading.tsu_readings():
                    new_readings.append(tsu_reading)
            readings = new_readings

        if prior and self.character == '々':
            for reading in prior.all_readings(first, last):
                readings.append(data.reading.Reading(
                    kanji=self,
                    kana=reading.kana,
                    type=reading.type,
                    is_rendaku=reading.is_rendaku,
                    is_tsu=reading.is_tsu,
                    base_reading=reading.base_reading
                ))

        return readings









