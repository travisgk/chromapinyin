# chromapinyin._syllable._inflection.py
# ---
# this file contains constant dictionaries that are used to
# process inflections and tones.
#
# an "inflection" refers to a more precise pronunciation of the tone.
# a "tone" refers to the innate tone of the character.
# so, tones range [-1, 4] and act the same as inflections,
# while anything above that range can only be referred to as an inflection.
#
# this file also contains the function <create_syllable_dict>,
# which will take a syllable in chinese represented
# by a single hanzi, its corresponding pinyin representation,
# and its contextual inflection to create and return a dictionary object with:
#
# 	- "hanzi": a string of the hanzi character
# 	- "pinyin": a string of the single pinyin syllable
# 	- "tone_str": a string describing the hanzi's innate tone.
# 	- "tone_num": the integer representation of the hanzi's innate tone.
# 	- "spoken_tone_str": a string describing the tone as its spoken.
# 	- "spoken_tone_num": the integer representation of the hanzi's innate tone.
# 	- "inflection_str": a string describing the spoken tone with added context.
# 	- "inflection_num": the integer representation of the contextual tone.
# 	- "ipa_root": the pinyin without tone transcribed in the IPA.
# 	- "ipa_suffix": the pinyin's spoken tone transcribed in the IPA.
# 	- "ipa": the entire IPA transcription with the spoken tone marker.
# 	- "zhuyin_prefix": the pinyin's tone marker that comes before (neutral tone).
# 	- "zhuyin_root": the pinyin without tone transcribed into zhuyin.
# 	- "zhuyin_suffix": the pinyin's tone marker than comes after.
# 	- "zhuyin": the entire zhuyin transcription.
#

from ._transcription import pinyin_to_zhuyin_and_ipa
from ._punctuation_marks import PUNCTUATION
from ._vowel_chars import (
	strip_tone_marker,
	APOSTROPHE_TONE_NUM,
	PUNCTUATION_TONE_NUM,
	HIGH_TONE_NUM,
	RISING_TONE_NUM,
	LOW_TONE_NUM,
	FALLING_TONE_NUM,
	NEUTRAL_TONE_NUM
)

# defines all the possible inflections used by the program.
TO_INFLECTION = {
	"apostrophe": APOSTROPHE_TONE_NUM,
	"punctuation": PUNCTUATION_TONE_NUM,
	"high": HIGH_TONE_NUM,
	"rising": RISING_TONE_NUM,
	"low": LOW_TONE_NUM,
	"falling": FALLING_TONE_NUM,
	"neutral": NEUTRAL_TONE_NUM,
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

# gives the inflection for a neutral tone that follows a primary tone.
TO_INFLECTED_NEUTRAL = {
	TO_INFLECTION["high"]: TO_INFLECTION["neutral_high"],
	TO_INFLECTION["rising"]: TO_INFLECTION["neutral_rising"],
	TO_INFLECTION["low"]: TO_INFLECTION["neutral_low"],
	TO_INFLECTION["falling"]: TO_INFLECTION["neutral_falling"],
}

# strips contextual information from the inflection.
INFLECTION_TO_SPOKEN_TONE = {
	TO_INFLECTION["apostrophe"]: TO_INFLECTION["punctuation"],
	TO_INFLECTION["punctuation"]: TO_INFLECTION["punctuation"],
	TO_INFLECTION["neutral"]: TO_INFLECTION["neutral_low"], # defaults
	TO_INFLECTION["high"]: TO_INFLECTION["high"],
	TO_INFLECTION["rising"]: TO_INFLECTION["rising"],
	TO_INFLECTION["low"]: TO_INFLECTION["low"],
	TO_INFLECTION["falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["full_low"]: TO_INFLECTION["full_low"],
	TO_INFLECTION["half_falling"]: TO_INFLECTION["half_falling"],
	TO_INFLECTION["neutral_high"]: TO_INFLECTION["neutral_high"],
	TO_INFLECTION["neutral_rising"]: TO_INFLECTION["neutral_rising"],
	TO_INFLECTION["neutral_low"]: TO_INFLECTION["neutral_low"],
	TO_INFLECTION["neutral_falling"]: TO_INFLECTION["neutral_falling"],
	TO_INFLECTION["rising_low"]: TO_INFLECTION["rising"],
	TO_INFLECTION["rising_yi"]: TO_INFLECTION["rising"],
	TO_INFLECTION["falling_yi"]: TO_INFLECTION["falling"],
	TO_INFLECTION["rising_bu"]: TO_INFLECTION["rising"],
}

# gives the inflection as its isolated innate tone.
_INFLECTION_TO_TONE = {
	TO_INFLECTION["apostrophe"]: TO_INFLECTION["punctuation"],
	TO_INFLECTION["punctuation"]: TO_INFLECTION["punctuation"],
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

# gives the spoken tone marker in the IPA.
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

# creates a dictionary object that contains information
# about a syllable in chinese.
def create_syllable_dict(hanzi, pinyin, inflection_num):
	tone_num = _INFLECTION_TO_TONE[inflection_num]
	spoken_tone_num = INFLECTION_TO_SPOKEN_TONE[inflection_num]
	syllable = {
		"hanzi": hanzi,
		"pinyin": pinyin,
		"tone_str": find_inflection_label(tone_num),
		"tone_num": tone_num,
		"spoken_tone_str": find_inflection_label(spoken_tone_num),
		"spoken_tone_num": spoken_tone_num,
		"inflection_str": find_inflection_label(inflection_num),
		"inflection_num": inflection_num,
		"ipa_root": "",
		"ipa_suffix": "",
		"ipa": "",
		"zhuyin_prefix": "",
		"zhuyin_root": "",
		"zhuyin_suffix": "",
		"zhuyin": "",
	}

	toneless_pinyin = strip_tone_marker(syllable["pinyin"])
	first_letter = toneless_pinyin[0]
	if first_letter in PUNCTUATION:
		syllable["ipa"] = first_letter
		if len(hanzi) > 0 and hanzi[0] in PUNCTUATION:
			syllable["zhuyin"] = hanzi[0]
		else:
			syllable["zhuyin"] = ""
		return syllable

	if not first_letter in "abcdefghjklmnopqrstwxyz":
		return syllable

	zhuyin_root, ipa_root = pinyin_to_zhuyin_and_ipa(toneless_pinyin)

	# transcribes pinyin into IPA.
	syllable["ipa_root"] = ipa_root
	syllable["ipa_suffix"] = _INFLECTION_TO_IPA_SUFFIX.get(inflection_num, "")
	syllable["ipa"] = ipa_root + syllable["ipa_suffix"]

	# transcribes pinyin into zhuyin.
	zhuyin_prefix = ""
	zhuyin_suffix = ""
	if spoken_tone_num == RISING_TONE_NUM:
		zhuyin_suffix = "ˊ"
	elif spoken_tone_num in [LOW_TONE_NUM, TO_INFLECTION["full_low"],]:
		zhuyin_suffix = "ˇ"
	elif spoken_tone_num in [FALLING_TONE_NUM, TO_INFLECTION["half_falling"],]:
		zhuyin_suffix = "ˋ"
	elif inflection_is_neutral(spoken_tone_num):
		zhuyin_prefix = "˙"
	
	syllable["zhuyin_prefix"] = zhuyin_prefix
	syllable["zhuyin_root"] = zhuyin_root
	syllable["zhuyin_suffix"] = zhuyin_suffix
	syllable["zhuyin"] = zhuyin_prefix + zhuyin_root + zhuyin_suffix
			
	return syllable

# returns a description of the contextual inflection 
# from its integer representation.
def find_inflection_label(inflection_num):
	for key, value in TO_INFLECTION.items():
		if inflection_num == value:
			return key
	return None

# returns True if an inflection is neutral.
def inflection_is_neutral(inflection_num):
	return(
		inflection_num == NEUTRAL_TONE_NUM 
		or inflection_num in TO_INFLECTED_NEUTRAL.values()
	)