import re
from ._vowel_chars import (
	get_tone_num, 
	is_pinyin_E, 
	is_pinyin_vowel, 
	_APOSTROPHE_TONE_NUM, 
	_NONE_TONE_NUM
)
from ._inflection import TO_INFLECTION, create_syllable_dict, _TO_INFLECTED_NEUTRAL
from ._punctuation_marks import PUNCTUATION, CLAUSE_BREAKS
import chromapinyin._sequential_inflection



_NORMAL_TONES = {
	TO_INFLECTION["high"],
	TO_INFLECTION["rising"],
	TO_INFLECTION["low"],
	TO_INFLECTION["falling"],
	TO_INFLECTION["neutral"],
}

# returns a list of groupings (lists) of dictionary objects.
# each dictionary object represents a syllable,
# which has the keys as defined in chromapinyin.inflection.py:
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
def create_list(hanzi_str, pinyin_str):
	# determines the groupings of initial inflections.
	inflections = []
	pinyin_list = split_pinyin(pinyin_str)
	for word in pinyin_list:
		inflections.append([])
		for syllable in word:
			tone_num = get_tone_num(syllable)
			inflections[-1].append(tone_num)

	# creates a 1D list of hanzi.
	hanzi_list = [
		char
		for unit in re.findall(r"[\w']+|[" + PUNCTUATION + "]", hanzi_str)
		for char in unit
	]

	# flattens the list of inflections to a 1D list.
	flat_inflections = [inflect for unit in inflections for inflect in unit]
	i = 0 # inflection index
	h = 0 # hanzi index

	VOICELESS = [_NONE_TONE_NUM, _APOSTROPHE_TONE_NUM]
	while i < len(flat_inflections) and h < len(hanzi_list):
		if (
			hanzi_list[h] not in PUNCTUATION 
			and flat_inflections[i] in VOICELESS
		):
			# current hanzi is not puncuation
			# but the current inflection is punctuation.
			i += 1
			continue

		elif hanzi_list[h] in PUNCTUATION:
			if flat_inflections[i] not in VOICELESS:
				# current hanzi is punctuation
				# but the current inflection is not punctuation.
				h += 1
				continue

			if flat_inflections[i] in VOICELESS:
				# current hanzi is punctuation
				# and the current inflection is punctuation as well.
				i += 1
				h += 1
				continue

		# hanzi and inflection are both not punctuation.
		if flat_inflections[i] == TO_INFLECTION["neutral"]:
			# neutral tone changes.
			if i - 1 >= 0 and flat_inflections[i - 1] not in VOICELESS:
				# previous inflection is not punctuation.
				_inflect_neutral(i, 1, flat_inflections)

			elif i - 2 >= 0 and flat_inflections[i - 2] not in VOICELESS:
				# previous inflection is punctuation 
				# but the inflection before that isn't.
				_inflect_neutral(i, 2, flat_inflections)

		elif i + 1 < len(flat_inflections):
			next_inflection = flat_inflections[i + 1]
			if hanzi_list[h] == "一":
				# checks if the inflection of "yi" should change.
				if next_inflection == TO_INFLECTION["falling"]:
					flat_inflections[i] = TO_INFLECTION["rising_yi"]
				elif next_inflection in _NORMAL_TONES:
					# next inflection is high, rising, or low.
					flat_inflections[i] = TO_INFLECTION["falling_yi"]
			elif (
				hanzi_list[h] == "不" 
				and next_inflection == TO_INFLECTION["falling"]
			):
				# bu must change inflection.
				flat_inflections[i] = TO_INFLECTION["rising_bu"]

		i += 1
		h += 1

	# copies the modified flat inflections list
	# back to the unflattened inflections list.
	flat_index = 0
	for i in range(len(inflections)):
		for j in range(len(inflections[i])):
			inflections[i][j] = flat_inflections[flat_index]
			flat_index += 1

	# applies 2-2-3 rule.
	chromapinyin._sequential_inflection.apply_rule(
		inflections, 
		TO_INFLECTION["low"],
		TO_INFLECTION["rising_low"]
	)

	# applies rule to make falling tones cut short.
	chromapinyin._sequential_inflection.apply_rule(
		inflections, 
		TO_INFLECTION["falling"],
		TO_INFLECTION["half_falling"]
	)

	# a low tone at the end of a clause will be inflected as a full low tone.
	for i in range(len(inflections)):
		# if the last inflection of the current unit is a low tone,
		# and 
		# 	it's at the end of the sentence
		#	or
		#		the unit right after is punctuation,
		#		and
		#			the unit comes at the very end,
		#			or the unit after that one is not neutral
		# then the last inflection of the current unit will be a full low tone.

		if (
			inflections[i][-1] == TO_INFLECTION["low"]
			and (
				i + 1 >= len(inflections)
				or(
					inflections[i + 1][0] == _APOSTROPHE_TONE_NUM
					and (
						i + 2 >= len(inflections) 
						or not is_neutral_tone(inflections[i + 2][0])
					)
				)
			)
		):
			inflections[i][-1] = TO_INFLECTION["full_low"]

	# unravels the inflections list again now that rules have been applied.
	flat_inflections = [inflect for unit in inflections for inflect in unit]

	# a list of groupings (lists) of syllable dictionaries 
	# are created and returned.
	syllable_results = []
	i = 0 # inflection index
	h = 0 # hanzi index
	for word in pinyin_list:
		syllable_results.append([])
		for pinyin_syllable in word:
			inflection = flat_inflections[i]

			if (
				h < len(hanzi_list) 
				and hanzi_list[h] not in PUNCTUATION 
				and inflection in [_NONE_TONE_NUM, _APOSTROPHE_TONE_NUM]
			):
				# current hanzi is not punctuation
				# but the current inflection is punctuation.
				# 
				syllable_results[-1].append(
					create_syllable_dict("", pinyin_syllable, inflection)
				)
			else:
				hanzi = hanzi_list[h] if h < len(hanzi_list) else ""
				syllable_results[-1].append(
					create_syllable_dict(hanzi, pinyin_syllable, inflection)
				)
				h += 1
			i += 1

	return syllable_results

# sets the inflection of the neutral tone 
# within <flat_inflections> at <current_index>
# to its inflected counterpart, based on the tone that
# comes <offset_backward> element(s) before <current_index>.
def _inflect_neutral(current_index, offset_backward, flat_inflections):
	i = current_index
	prev_i = current_index - offset_backward

	# the previous inflection is not punctuation.
	if flat_inflections[prev_i] in _NORMAL_TONES:
		# the previous inflection is a normal tone.
		# sets current inflection to the corresponding neutral.
		flat_inflections[i] = _TO_INFLECTED_NEUTRAL[flat_inflections[prev_i]]

	elif flat_inflections[prev_i] in _TO_INFLECTED_NEUTRAL.items():
		# <prev_inflection> is an inflected neutral.
		# the current inflection just repeats it.
		flat_inflections[i] = flat_inflections[prev_i]

# returns a list of units, 
# with each unit (word) containing strings of pinyin syllables.
def split_pinyin(pinyin_str):
	results = []

	# breaks <pinyin_str> into a list, with <CLAUSE_BREAKS>
	# becoming their own elements.
	words = re.findall(r"[\w']+|[" + CLAUSE_BREAKS + "]", pinyin_str)

	for word in words:
		units = []
		substrings = re.split(r"[\']", word)

		# inserts an apostrophe between substrings.
		units = (
			[sub for sub in substrings[: -1]] + ["'"] + [substrings[-1]]
			if len(substrings) > 1
			else substrings
		)

		# appends a list of syllable dictionaries to the <results> list.
		results.append([])
		for unit_str in units:
			_word_unit_to_syllables(results, unit_str)

	return results

# processes the given <unit_str> and breaks it down
# into syllables and appends the unit
# to the <results> list of units.	
def _word_unit_to_syllables(results, unit_str):
	if unit_str[0] in PUNCTUATION:
		# adds punctuation.
		results[-1].append(unit_str[0])
		return

	# syllable is a word.
	while len(unit_str) > 0:
		# "er" is exceptional.
		if is_pinyin_E(unit_str[0]) and unit_str[1] in "Rr":
			results[-1].append(unit_str[:2])
			unit_str = unit_str[2:]
			continue

		for i, char in enumerate(unit_str):
			if i == len(unit_str) - 1:
				# last character.
				results[-1].append(unit_str)
				unit_str = ""
				break

			elif (
				not is_pinyin_vowel(char) 
				and any(is_pinyin_vowel(letter) for letter in unit_str[:i])
			):
				# the consonant <char> is preceded by a vowel.
				# this indicates that the <unit_str> 
				# can be broken into further syllables.
				unit_str = _break_down_unit_str(results, unit_str, i)
				break

# returns what remains of the given <unit_str> 
# after trying to break a left section of the string
# and adding it to the given <results> list of units.
def _break_down_unit_str(results, unit_str, i):
	if not any(is_pinyin_vowel(letter) for letter in unit_str[i:]):
		# (e)bbb..|
		results[-1].append(unit_str)
		return ""

	# a vowel follows the consonant <unit_str[i]>.
	# now it's determined how 'n' and 'ng' 
	# break up into syllables.
	if unit_str[i] in "Nn":
		if unit_str[i + 1] in "Gg":
			# (e)ng(e)
			if is_pinyin_vowel(unit_str[i + 2]):
				# (e)n|g(e)
				results[-1].append(unit_str[: i + 1])
				return unit_str[i + 1 :]
			else:
				# (e)ng|(b)(e)
				results[-1].append(unit_str[: i + 2])
				return unit_str[i + 2 :]
		else:
			# (e)n(e)
			if is_pinyin_vowel(unit_str[i + 1]):
				# (e)|n(e)
				results[-1].append(unit_str[:i])
				return unit_str[i:]
			else:
				# (e)n|(b)(e)
				results[-1].append(unit_str[: i + 1])
				return unit_str[i + 1 :]

	# (e)|b(e)
	results[-1].append(unit_str[:i])
	return unit_str[i:]
		