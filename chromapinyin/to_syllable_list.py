import re
from .vowel_chars import is_pinyin_E, is_pinyin_vowel
from .punctuation_marks import PUNCTUATION

CLAUSE_BREAKS = "。，！？；：、．.,!-?;:"

def split_pinyin(pinyin_text):
	results = []

	# breaks <pinyin_text> into a list, with <CLAUSE_BREAKS>
	# becoming their own elements.
	words = re.findall(r"[\w']+|[" + CLAUSE_BREAKS + "]", pinyin_text)

	for word in words:
		units = []
		substrings = re.split(r"[\']", word)

		# inserts an apostrophe between substrings.
		if len(substrings) > 1:
			units = (
				[sub for sub in substrings[: -1]] + ["'"] + [substrings[-1]]
			)
		else:
			units = substrings

		# appends a list of syllable dictionaries to the <results> list.
		results.append([])
		for unit_str in units:
			_word_unit_to_syllables(results, unit_str)
	return results
			
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
				if any(is_pinyin_vowel(letter) for letter in unit_str[i:]):
					# a vowel follows the consonant <char>.
					# now it's determined how 'n' and 'ng' 
					# break up into syllables.
					if char in "Nn":
						if unit_str[i + 1] in "Gg":
							# (e)ng(e)
							if is_pinyin_vowel(unit_str[i + 2]):
								# (e)n|g(e)
								results[-1].append(unit_str[: i + 1])
								unit_str = unit_str[i + 1 :]
							else:
								# (e)ng|(b)(e)
								results[-1].append(unit_str[: i + 2])
								unit_str = unit_str[i + 2 :]
						else:
							# (e)n(e)
							if is_pinyin_vowel(unit_str[i + 1]):
								# (e)|n(e)
								results[-1].append(unit_str[:i])
								unit_str = unit_str[i:]
							else:
								# (e)n|(b)(e)
								results[-1].append(unit_str[: i + 1])
								unit_str = unit_str[i + 1 :]
					else:
						# (e)|b(e)
						results[-1].append(unit_str[:i])
						unit_str = unit_str[i:]
				else:
					# (e)bbb..|
					results[-1].append(unit_str)
					unit_str = ""
				break