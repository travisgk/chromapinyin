import os
from ._punctuation_marks import PUNCTUATION
from ._vowel_chars import (
	strip_tone_marker,
	_NONE_TONE_NUM,
	_HIGH_TONE_NUM,
	_RISING_TONE_NUM,
	_LOW_TONE_NUM,
	_FALLING_TONE_NUM,
	_NEUTRAL_TONE_NUM
)

# an "inflection" refers to a more precise pronunciation of the tone.
# a "tone" refers to the innate tone of the character.
# so, tones range [-1, 4] and act the same as inflections,
# while anything above that range can only be referred to as an inflection.
TO_INFLECTION = {
	"none": _NONE_TONE_NUM, # punctuation
	"high": _HIGH_TONE_NUM,
	"rising": _RISING_TONE_NUM,
	"low": _LOW_TONE_NUM,
	"falling": _FALLING_TONE_NUM,
	"neutral": _NEUTRAL_TONE_NUM,
	"full_low": 6, # a low tone at the end of a clause
	"half_falling": 7,
	"neutral_high": 8, # neutral following a high tone
	"neutral_rising": 9, # neutral following a rising tone
	"neutral_low": 10, # neutral following a low tone
	"neutral_falling": 11, # neutral following a falling tone
	"rising_low": 12, # a low tone following the 2-2-3 rule
	"rising_yi": 13,
	"falling_yi": 14,
	"rising_bu": 15,
}

_TO_INFLECTED_NEUTRAL = {
	TO_INFLECTION["high"]: TO_INFLECTION["neutral_high"],
	TO_INFLECTION["rising"]: TO_INFLECTION["neutral_rising"],
	TO_INFLECTION["low"]: TO_INFLECTION["neutral_low"],
	TO_INFLECTION["falling"]: TO_INFLECTION["neutral_falling"],
}

_INFLECTION_TO_TONE = {
	TO_INFLECTION["none"]: TO_INFLECTION["none"],
	TO_INFLECTION["neutral"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["high"]: TO_INFLECTION["high"],
	TO_INFLECTION["rising"]: TO_INFLECTION["rising"],
	TO_INFLECTION["low"]: TO_INFLECTION["low"],
	TO_INFLECTION["falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["full_low"]: TO_INFLECTION["low"],
	TO_INFLECTION["half_falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["neutral_high"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_rising"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_low"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_falling"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["rising_low"]: TO_INFLECTION["low"],
	TO_INFLECTION["rising_yi"]: TO_INFLECTION["high"],
	TO_INFLECTION["falling_yi"]: TO_INFLECTION["high"],
	TO_INFLECTION["rising_bu"]: TO_INFLECTION["low"],
}

_INFLECTION_TO_SPOKEN_TONE = {
	TO_INFLECTION["none"]: TO_INFLECTION["none"],
	TO_INFLECTION["neutral"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["high"]: TO_INFLECTION["high"],
	TO_INFLECTION["rising"]: TO_INFLECTION["rising"],
	TO_INFLECTION["low"]: TO_INFLECTION["low"],
	TO_INFLECTION["falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["full_low"]: TO_INFLECTION["low"],
	TO_INFLECTION["half_falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["neutral_high"]: TO_INFLECTION["neutral_high"],
	TO_INFLECTION["neutral_rising"]: TO_INFLECTION["neutral_rising"],
	TO_INFLECTION["neutral_low"]: TO_INFLECTION["neutral_low"],
	TO_INFLECTION["neutral_falling"]: TO_INFLECTION["neutral_falling"],
	TO_INFLECTION["rising_low"]: TO_INFLECTION["rising"],
	TO_INFLECTION["rising_yi"]: TO_INFLECTION["rising"],
	TO_INFLECTION["falling_yi"]: TO_INFLECTION["falling"],
	TO_INFLECTION["rising_bu"]: TO_INFLECTION["rising"],
}

_INFLECTION_TO_IPA_SUFFIX = {
	TO_INFLECTION["high"]: "˥",
	TO_INFLECTION["rising"]: "˧˥",
	TO_INFLECTION["rising_low"]: "˧˥",
	TO_INFLECTION["rising_yi"]: "˧˥",
	TO_INFLECTION["rising_bu"]: "˧˥",
	TO_INFLECTION["low"]: "˨˩",
	TO_INFLECTION["full_low"]: "˨˩˦",
	TO_INFLECTION["falling"]: "˥˩",
	TO_INFLECTION["falling_yi"]: "˥˩",
	TO_INFLECTION["half_falling"]: "˥˧",
	TO_INFLECTION["neutral"]: "꜌",
	TO_INFLECTION["neutral_high"]: "꜋",
	TO_INFLECTION["neutral_rising"]: "꜊",
	TO_INFLECTION["neutral_low"]: "꜉",
	TO_INFLECTION["neutral_falling"]: "꜌",
}

def _find_inflection_label(inflection_num):
	for key, value in TO_INFLECTION.items():
		if inflection_num == value:
			return key
	return None

# creates a dictionary object that contains information
# about a syllable in Mandarin.
#
# the files in ~/transcription are used to set
# the phonetic pronunciation (IPA) and the zhuyin.
#
# "hanzi": the syllable written in hanzi.
# "pinyin": the syllable written in pinyin.
# "tone": a description of innate tone.
# "tone_num": the number used by the program to refer to this tone.
# "spoken_tone": a description of the spoken tone. 
# "spoken_tone_num": the number used by the program to refer to this tone.
# "inflection": a description of the contextual inflection.
# "inflection_num": the number used by the program to refer to the inflection.
# "ipa": the syllable transcribed in the international phonetic alphabet.
# "zhuyin": the syllable transcribed in zhuyin.
def create_syllable_dict(hanzi, pinyin, inflection_num):
	tone_num = _INFLECTION_TO_TONE[inflection_num]
	spoken_tone_num = _INFLECTION_TO_SPOKEN_TONE[inflection_num]
	syllable = {
		"hanzi": hanzi,
		"pinyin": pinyin,
		"tone": _find_inflection_label(tone_num),
		"tone_num": tone_num,
		"spoken_tone": _find_inflection_label(spoken_tone_num),
		"spoken_tone_num": spoken_tone_num,
		"inflection": _find_inflection_label(inflection_num),
		"inflection_num": inflection_num,
		"ipa_root": "",
		"ipa_suffix": "",
		"ipa": "",
		"zhuyin_prefix": "",
		"zhuyin_root": "",
		"zhuyin_suffix": "",
		"zhuyin": "",
	}

	stripped_pinyin = strip_tone_marker(syllable["pinyin"])
	first_letter = stripped_pinyin[0]
	if first_letter in PUNCTUATION and hanzi[0] in PUNCTUATION:
		syllable["ipa"] = first_letter
		syllable["zhuyin"] = hanzi[0]
		return syllable

	if not first_letter in "abcdefghjklmnopqrstwxyz":
		return syllable

	script_dir = os.path.dirname(os.path.realpath(__file__))
	file_name = os.path.join(
		script_dir, "transcription/_phonemes_" + first_letter + ".txt"
	)
	
	if not os.path.isfile(file_name):
		print(f"Could not find {file_name}.")

		return syllable

	with open(file_name, "r", encoding="utf-8") as file:
		for line in file:
			contents = line.rstrip().split("\t")
			pinyin, ipa_root, zhuyin_root = contents
			if stripped_pinyin != pinyin:
				continue

			# transcribes pinyin into IPA.
			syllable["ipa_root"] = ipa_root
			syllable["ipa_suffix"] = _INFLECTION_TO_IPA_SUFFIX.get(
				inflection_num, ""
			)
			syllable["ipa"] = ipa_root + syllable["ipa_suffix"]

			# transcribes pinyin into zhuyin.
			zhuyin_prefix = ""
			zhuyin_suffix = ""
			if spoken_tone_num == _RISING_TONE_NUM:
				zhuyin_suffix = "ˊ"
			elif spoken_tone_num == _LOW_TONE_NUM:
				zhuyin_suffix = "ˇ"
			elif spoken_tone_num == _FALLING_TONE_NUM:
				zhuyin_suffix = "ˋ"
			elif (
				spoken_tone_num == _NEUTRAL_TONE_NUM 
				or spoken_tone_num in _INFLECTION_TO_SPOKEN_TONE.values()
			):
				zhuyin_prefix = "˙"
			
			syllable["zhuyin_prefix"] = zhuyin_prefix
			syllable["zhuyin_root"] = zhuyin_root
			syllable["zhuyin_suffix"] = zhuyin_suffix
			syllable["zhuyin"] = zhuyin_prefix + zhuyin_root + zhuyin_suffix

			break
			
	return syllable