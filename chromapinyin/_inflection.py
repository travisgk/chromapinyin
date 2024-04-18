import os
from .vowel_chars import strip_tone_marker

ADD_TONE_MARKERS_TO_IPA = False
ADD_TONE_MARKERS_TO_ZHUYIN = True

TO_INFLECTION = {
	"none": -1,
	"neutral": 0,
	"high": 1,
	"rising": 2,
	"low": 3,
	"falling": 4,
	"full_low": 5,
	"half_falling": 6,
	"neutral_high": 7, # neutral following a high tone
	"neutral_rising": 8, # neutral following a rising tone
	"neutral_low": 9, # neutral following a low tone
	"neutral_falling": 10, # neutral following a falling tone
	"rising_low": 11,
	"yi_rising": 12,
	"yi_falling": 13,
	"bu_rising": 14,
}

INFLECTION_TO_TONE = {
	-1: -1,
	0: 0,
	1: 1,
	2: 2,
	3: 3,
	4: 4,
	5: 3,
	6: 4,
	7: 0,
	8: 0,
	9: 0,
	10: 0,
	11: 3,
	12: 1,
	13: 1,
	14: 3,
}

INFLECTION_TO_IPA_SUFFIX = {
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

def find_inflection_label(inflection):
	for key, value in TO_INFLECTION.items():
		if inflection == value:
			return key
	return None

def is_neutral_inflection(i):
	return (
		i == TO_INFLECTION["none"] 
		or TO_INFLECTION["neutral_high"] <= i <= TO_INFLECTION["neutral_falling"]
	)

# uses the files in ~/transcription 
# to set the phonetic pronunciation (IPA) and the zhuyin.
def create_syllable_dict(hanzi, pinyin, inflection):
	syllable = {"hanzi": hanzi, "pinyin": pinyin, "inflection": inflection}
	stripped_pinyin = strip_tone_marker(syllable["pinyin"])
	first_letter = stripped_pinyin[0]
	if not first_letter in "abcdefghjklmnopqrstwxyz":
		return

	script_dir = os.path.dirname(os.path.realpath(__file__))
	print(script_dir)
	file_name = os.path.join(script_dir, "transcription/_phonemes_" + first_letter + ".txt")
	
	if not os.path.isfile(file_name):
		print(f"Could not find {file_name}.")
		return

	with open(file_name, "r", encoding="utf-8") as file:
		for line in file:
			contents = line.rstrip().split("\t")
			pinyin, ipa, zhuyin = contents
			if stripped_pinyin != pinyin:
				continue

			if ADD_TONE_MARKERS_TO_IPA:
				suffix = INFLECTION_TO_IPA_SUFFIX.get(inflection, "")
				syllable["ipa"] = ipa + suffix
			else:
				syllable["ipa"] = ipa

			if ADD_TONE_MARKERS_TO_ZHUYIN:
				prefix = ""
				suffix = ""
				tone_num = INFLECTION_TO_TONE[inflection]
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

def print_syllable_dict():
	hanzi = syllable["hanzi"]
	pinyin = syllable["pinyin"]
	inflection_str = find_inflection_label(syllable["inflection"])
	ipa = syllable["ipa"]
	zhuyin = syllable["zhuyin"]
	return f"({hanzi},\t{pinyin},\t{inflection_str},\t{ipa},\t{zhuyin})"
