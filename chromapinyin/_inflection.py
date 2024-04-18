import os
from .vowel_chars import strip_tone_marker

ADD_TONE_MARKERS_TO_IPA = False
ADD_TONE_MARKERS_TO_ZHUYIN = True

# an "inflection" refers to a more precise pronunciation of the tone.
# a "tone" refers to the innate tone of the character.
# so, tones range [-1, 4] and act the same as inflections,
# while anything above that range can only be referred to as an inflection.
TO_INFLECTION = {
	"none": -1, # punctuation
	"neutral": 0,
	"high": 1,
	"rising": 2,
	"low": 3,
	"falling": 4,
	"full_low": 5, # a low tone at the end of a clause
	"half_falling": 6,
	"neutral_high": 7, # neutral following a high tone
	"neutral_rising": 8, # neutral following a rising tone
	"neutral_low": 9, # neutral following a low tone
	"neutral_falling": 10, # neutral following a falling tone
	"rising_low": 11, # a low tone following the 2-2-3 rule
	"yi_rising": 12,
	"yi_falling": 13,
	"bu_rising": 14,
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
	TO_INFLECTION["yi_rising"]: TO_INFLECTION["high"],
	TO_INFLECTION["yi_falling"]: TO_INFLECTION["high"],
	TO_INFLECTION["bu_rising"]: TO_INFLECTION["low"],
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
	TO_INFLECTION["neutral_high"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_rising"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_low"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_falling"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["rising_low"]: TO_INFLECTION["rising"],
	TO_INFLECTION["yi_rising"]: TO_INFLECTION["rising"],
	TO_INFLECTION["yi_falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["bu_rising"]: TO_INFLECTION["rising"],
}

_INFLECTION_TO_IPA_SUFFIX = {
	TO_INFLECTION["high"]: "˥",
	TO_INFLECTION["rising"]: "˧˥",
	TO_INFLECTION["rising_low"]: "˧˥",
	TO_INFLECTION["yi_rising"]: "˧˥",
	TO_INFLECTION["bu_rising"]: "˧˥",
	TO_INFLECTION["low"]: "˨˩",
	TO_INFLECTION["full_low"]: "˨˩˦",
	TO_INFLECTION["falling"]: "˥˩",
	TO_INFLECTION["yi_falling"]: "˥˩",
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
	}
	stripped_pinyin = strip_tone_marker(syllable["pinyin"])
	first_letter = stripped_pinyin[0]
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
			pinyin, ipa, zhuyin = contents
			if stripped_pinyin != pinyin:
				continue

			if ADD_TONE_MARKERS_TO_IPA:
				suffix = INFLECTION_TO_IPA_SUFFIX.get(inflection_num, "")
				syllable["ipa"] = ipa + suffix
			else:
				syllable["ipa"] = ipa

			if ADD_TONE_MARKERS_TO_ZHUYIN:
				prefix = ""
				suffix = ""
				if tone_num == 2: # rising tone
					suffix = "ˊ"
				elif tone_num == 3: # low tone
					suffix = "ˇ"
				elif tone_num == 4: # falling tone
					suffix = "ˋ"
				elif tone_num == 0: # neutral tone
					prefix = "˙"

				syllable["zhuyin"] = prefix + zhuyin + suffix
			else:
				syllable["zhuyin"] = zhuyin
			break
	return syllable