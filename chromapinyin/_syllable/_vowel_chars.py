# chromapinyin._syllable._vowel_chars.py
# ---
# this file contains constant integers which represent primary tones in chinese,
# as well as functions relating to pinyin and tone markers.
#

from ._punctuation_marks import APOSTROPHES, PUNCTUATION

APOSTROPHE_TONE_NUM = -1
PUNCTUATION_TONE_NUM = 0
HIGH_TONE_NUM = 1
RISING_TONE_NUM = 2
LOW_TONE_NUM = 3
FALLING_TONE_NUM = 4
NEUTRAL_TONE_NUM = 5

PRIMARY_TONES = [
    HIGH_TONE_NUM,
    RISING_TONE_NUM,
    LOW_TONE_NUM,
    FALLING_TONE_NUM,
]

_VOWELS = [
    "AĀÁǍÀ",
    "aāáǎà",
    "OŌÓǑÒ",
    "oōóǒò",
    "EĒÉĚÈ",
    "eēéěè",
    "IĪÍǏÌ",
    "iīíǐì",
    "UŪÚǓÙ",
    "uūúǔù",
    "ÜǕǗǙǛ",
    "üǖǘǚǜ",
]

_TONE_TO_TONELESS = {
    "Ā": "A",
    "Á": "A",
    "Ǎ": "A",
    "À": "A",
    "ā": "a",
    "á": "a",
    "ǎ": "a",
    "à": "a",
    "Ō": "O",
    "Ó": "O",
    "Ǒ": "O",
    "Ò": "O",
    "ō": "o",
    "ó": "o",
    "ǒ": "o",
    "ò": "o",
    "Ē": "E",
    "É": "E",
    "Ě": "E",
    "È": "E",
    "ē": "e",
    "é": "e",
    "ě": "e",
    "è": "e",
    "Ī": "I",
    "Í": "I",
    "Ǐ": "I",
    "Ì": "I",
    "ī": "i",
    "í": "i",
    "ǐ": "i",
    "ì": "i",
    "Ū": "U",
    "Ú": "U",
    "Ǔ": "U",
    "Ù": "U",
    "ū": "u",
    "ú": "u",
    "ǔ": "u",
    "ù": "u",
    "Ǖ": "Ü",
    "Ǘ": "Ü",
    "Ǚ": "Ü",
    "Ǜ": "Ü",
    "ǖ": "ü",
    "ǘ": "ü",
    "ǚ": "ü",
    "ǜ": "ü",
}

_VOWEL_TO_TONE_NUM = {
    "Ā": 1,
    "Á": 2,
    "Ǎ": 3,
    "À": 4,
    "ā": 1,
    "á": 2,
    "ǎ": 3,
    "à": 4,
    "Ō": 1,
    "Ó": 2,
    "Ǒ": 3,
    "Ò": 4,
    "ō": 1,
    "ó": 2,
    "ǒ": 3,
    "ò": 4,
    "Ē": 1,
    "É": 2,
    "Ě": 3,
    "È": 4,
    "ē": 1,
    "é": 2,
    "ě": 3,
    "è": 4,
    "Ī": 1,
    "Í": 2,
    "Ǐ": 3,
    "Ì": 4,
    "ī": 1,
    "í": 2,
    "ǐ": 3,
    "ì": 4,
    "Ū": 1,
    "Ú": 2,
    "Ǔ": 3,
    "Ù": 4,
    "ū": 1,
    "ú": 2,
    "ǔ": 3,
    "ù": 4,
    "Ǖ": 1,
    "Ǘ": 2,
    "Ǚ": 3,
    "Ǜ": 4,
    "ǖ": 1,
    "ǘ": 2,
    "ǚ": 3,
    "ǜ": 4,
}


def is_pinyin_vowel(char):
    return char in [vowel for line in _VOWELS for vowel in line]


def is_pinyin_E(char):
    return char in [vowel for line in _VOWELS[4:6] for vowel in line]


# returns a number indicating the pinyin syllable's tone.
# 0 for none, 1 for high, 2 for rising, 3 for low, 4 for falling, 5 for neutral.
def get_tone_num(syllable_str):
    if syllable_str[0] in APOSTROPHES:
        return APOSTROPHE_TONE_NUM
    if syllable_str[0] in PUNCTUATION:
        return PUNCTUATION_TONE_NUM
    for char in syllable_str:
        tone_num = _VOWEL_TO_TONE_NUM.get(char)
        if tone_num is not None:
            return tone_num
    return NEUTRAL_TONE_NUM


# returns a syllable string with all accent marks removed.
def strip_tone_marker(syllable_str):
    return "".join([_TONE_TO_TONELESS.get(char, char) for char in syllable_str])


# returns the given pinyin syllable string with an applied tone marker.
def place_tone_marker(syllable_str, tone_num):
    if not tone_num in PRIMARY_TONES:
        return syllable_str

    for i, char in enumerate(syllable_str):
        for line in _VOWELS:
            if char not in line:
                continue

            if (
                char in "Ii"
                and i + 1 < len(syllable_str)
                and syllable_str[i + 1] in "Uu"
            ):
                # with "iu", the tone marker will go above the "u".
                return syllable_str[: i + 1] + line[tone_num] + syllable_str[i + 2 :]

            # otherwise, the tone marker goes above the first found vowel.
            return syllable_str[:i] + line[tone_num] + syllable_str[i + 1 :]
    return syllable_str
