# sequential_inflection.py
# ---
# this file defines a function used to make inflections
# follow the 2-2-3 rule in Mandarin.
# this is an approximation; regional variance is bound to differ.
#

from ._inflection import TO_INFLECTION, _TO_INFLECTED_NEUTRAL, _NEUTRAL_TONE_NUM
from ._vowel_chars import _APOSTROPHE_TONE_NUM, _NONE_TONE_NUM

_PRINT_APPLY_RULE_DEBUG = False

# modifies the given list of inflections groupings
# to follow the sequential inflection rule, 
# most commonly seen in the 2-2-3 pattern in sequential low tones.
def apply_rule(inflection_groups, stay_inflection, to_inflection):
	NONE = _NONE_TONE_NUM # indicates a tone that is irrelevant
	APOSTROPHE = _APOSTROPHE_TONE_NUM
	UNDETERMINED = 99 # indicates a tone which will be determined

	# creates a list of inflections without apostrophes.
	inflections = [
		[inf for inf in g if inf != APOSTROPHE] for g in inflection_groups
	]

	# creates a mark-up list.
	markup_clause = [
		[
			UNDETERMINED 
			if inflection == stay_inflection 
			else NONE for inflection in word
		] for word in inflections
	]
	if all(mark == NONE for word in markup_clause for mark in word):
		return

	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(0, markup_clause, stay_inflection, to_inflection)

	# 1) if the inflection is the last occurrence
	#    in-a-row in the overall clause, then it remains <stay_inflection>.
	#
	for i, word in enumerate(markup_clause):
		for j in range(len(word)): 
			# <word> is a list of inflections.
			if word[j] != UNDETERMINED:
				continue
			
			# an UNDETERMINED occurrence will remain <stay_inflection> if:
			#
			# the UNDETERMINED occurrence is at the very end of the clause,
			#
			# or the UNDETERMINED occurrence is not at the end of the <word>
			# and the following syllable isn't marked UNDETERMINED
			#
			# or the current <word> is not at the end of the clause
			# and
			#	the UNDETERMINED occurrence is at the end of the <word>
			#	and the following beginning syllable
			#	of the next word in the clause is marked NONE
			#
			#	or
			#
			#	the next occurrence in the original <inflections> list
			#	does not have any inflection (is punctuation)
			#	and
			#		there's no further occurrence after the punctuation
			#
			#		or 
			#
			#		the occurrence after the punctuation is neutral
			#
			if (
				(i == len(markup_clause) - 1 and j == len(word) - 1)
				or (j + 1 < len(word) and word[j + 1] != UNDETERMINED)
				or (
					j == len(word) - 1
					and i + 1 < len(markup_clause)
					and inflections[i + 1][0] != UNDETERMINED
					and (
						i + 2 >= len(markup_clause)
						or _is_neutral_inflection(inflections[i + 2][0])
						or inflections[i + 2] == TO_INFLECTION['none']
					)
				)
			):
				markup_clause[i][j] = stay_inflection
	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(1, markup_clause, stay_inflection, to_inflection)

	# 2) in a series of UNDETERMINED marks under one multisyllable word,
	#    every UNDETERMINED tone in the series is marked as <to_inflection>,
	#    except for if that UNDETERMINED 
	#
	for i, word in enumerate(markup_clause):
		if len(word) > 1:
			for j in range(len(word) - 1):
				if markup_clause[i][j] == UNDETERMINED:
					markup_clause[i][j] = to_inflection
	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(2, markup_clause, stay_inflection, to_inflection)

	# 3) a series of two or more UNDETERMINED monosyllable tones are filled:
	#    <to...>, <src...>, <to...>, <to...>, <src...>
	#    <to...>, <src...>,          <to...>, <src...>
	#    depending on if the series' length is odd or even respectively.
	#
	monosyllable_series = _find_series_of_monosyllables(
		markup_clause, [stay_inflection, to_inflection, UNDETERMINED]
	)
	for current_series in monosyllable_series:
		if len(current_series) <= 1:
			continue

		changes = True
		for i, occurrence in enumerate(current_series):
			occurrences_left = len(current_series) - 1 - i
			if occurrences_left == 1 and not changes:
				changes = True

			w, s = occurrence
			if markup_clause[w][s] == UNDETERMINED:
				markup_clause[w][s] = (
					to_inflection if changes else stay_inflection
				)

			changes = not changes
	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(3, markup_clause, stay_inflection, to_inflection)

	# 4) an UNDETERMINED mark will become <to_inflection> if
	#    the inflection that comes before or after it is <stay_inflection>
	#    and both of these neighboring inflections are not UNDETERMINED.
	for i, word in enumerate(markup_clause):
		for j in range(len(word)):
			if word[j] != UNDETERMINED:
				continue

			next_inflection = UNDETERMINED
			if j + 1 < len(word):
				next_inflection = word[j + 1]
			elif i + 1 < len(markup_clause):
				next_inflection = markup_clause[i + 1][0]

			if next_inflection == UNDETERMINED:
				continue

			# sets inflection using neighbors.
			if i == 0 and j == 0:
				# sets the first inflection if next one is known.
				markup_clause[i][j] = (
					to_inflection 
					if next_inflection == stay_inflection 
					else stay_inflection
				)
			else:
				prev_inflection = UNDETERMINED
				if j - 1 >= 0:
					prev_inflection = word[j - 1]
				elif i - 1 >= 0:
					prev_inflection = markup_clause[i - 1][-1]

				if prev_inflection == UNDETERMINED:
					continue

				# sets the inflection using its neighbors if they are known.
				if (
					prev_inflection == stay_inflection 
					or next_inflection == stay_inflection
				):
					markup_clause[i][j] = to_inflection
				else:
					markup_clause[i][j] = stay_inflection
	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(4, markup_clause, stay_inflection, to_inflection)

	# 5) evaluating right-to-left, if one of the two rightward marks
	#    of an UNDETERMINED mark is <stay_inflection>, 
	#    then the UNDETERMINED mark becomes <to_inflection>.
	#    otherwise, the UNDETERMINED mark becomes <stay_inflection>.
	for i in range(len(markup_clause) - 1, -1, -1):
		word = markup_clause[i]
		for j in range(len(word) - 1, -1, -1):
			if word[j] != UNDETERMINED:
				continue

			# searches rightward within <word> and immediately 
			# after <word> for an <to_inflection> mark.
			if j + 1 < len(word):
				if word[j + 1] == stay_inflection:
					markup_clause[i][j] = to_inflection
				else:
					if j + 2 < len(word):
						markup_clause[i][j] = (
							stay_inflection
							if word[j + 2] == to_inflection
							else to_inflection
						)
					elif i + 1 < len(markup_clause):
						markup_clause[i][j] = (
							stay_inflection
							if markup_clause[i + 1][0] == to_inflection
							else to_inflection
						)

			# searches rightward outside <word> for an <to_inflection> mark.
			elif i + 1 < len(markup_clause):
				next_word = markup_clause[i + 1]
				if next_word[0] == stay_inflection:
					markup_clause[i][j] = to_inflection
				else:
					if len(next_word) > 1:
						markup_clause[i][j] = (
							stay_inflection
							if next_word[1] == to_inflection
							else to_inflection
						)

					# searches word after <next_word>.
					elif i + 2 < len(markup_clause):
						markup_clause[i][j] = (
							stay_inflection
							if markup_clause[i + 2][0] == to_inflection
							else to_inflection
						)
	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(5, markup_clause, stay_inflection, to_inflection)

	# 6) if a series of three monosyllables has a prior tone 
	#    that's nonexistent or NONE, and the series is composed of
	#    a combination of <to_inflection> and <stay_inflection> such that:
	#
	#    (NONE), <to...>, <to...>, <src...>
	#    (NONE), <to...>, <to...>, <to...>
	#
	#    then the first occurrence of the monosyllable series 
	#    will become <stay_inflection>.
	#
	for current_series in monosyllable_series:
		if len(current_series) != 3:
			continue

		w_0, s_0 = current_series[0]
		w_1, s_1 = current_series[1]
		w_2, s_2 = current_series[2]

		syllable_0 = markup_clause[w_0][s_0]
		syllable_1 = markup_clause[w_1][s_1]
		syllable_2 = markup_clause[w_2][s_2]

		if (
			syllable_0 == to_inflection
			and syllable_1 == to_inflection
			and syllable_2 in [stay_inflection, to_inflection]
			and (w_0 == 0 or inflections[w_0 - 1][-1] == NONE)
		):
			markup_clause[w_0][s_0] = to_inflection
	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(6, markup_clause, stay_inflection, to_inflection)

	# 7) if a series of four monosyllables has a prior tone
	#    that's nonexistent or NONE, and the series is composed of
	#    a combination of  <to_inflection> or <stay_inflection> such that:
	#
	#    (NONE), <to...>, <src...>, <to...>, <src...>
	#
	#    then the first inflection becomes <stay_inflection>
	#    and the second inflection becomes <to_inflection>.
	for current_series in monosyllable_series:
		if len(current_series) != 4:
			continue

		w_0, s_0 = current_series[0]
		w_1, s_1 = current_series[1]
		w_2, s_2 = current_series[2]
		w_3, s_3 = current_series[3]

		syllable_0 = markup_clause[w_0][s_0]
		syllable_1 = markup_clause[w_1][s_1]
		syllable_2 = markup_clause[w_2][s_2]
		syllable_3 = markup_clause[w_3][s_3]

		if (
			syllable_0 == to_inflection
			and syllable_1 == stay_inflection
			and syllable_2 == to_inflection
			and syllable_3 == stay_inflection
			and (w_0 == 0 or inflections[w_0 - 1][-1] == NONE)
			and (
				w_3 + 1 >= len(markup_clause)
				or (
					len(markup_clause[w_3 + 1]) == 1
					and markup_clause[w_3 + 1][0] == NONE
				)
				or (
					markup_clause[w_3 + 1][0] != to_inflection
				)
			)
		):
			markup_clause[w_0][s_0] = stay_inflection
			markup_clause[w_1][s_1] = to_inflection
	if _PRINT_APPLY_RULE_DEBUG:
		_print_markup_clause(7, markup_clause, stay_inflection, to_inflection)

	# copies the inflections to the given original <inflection_groups> list,
	# only if the inflection in the <markup_clause> was determined.
	for i, mark_word in enumerate(markup_clause):
		mark_j = 0
		for inflection_j in range(len(inflection_groups[i])):
			if inflection_groups[i][inflection_j] == APOSTROPHE:
				continue
			if mark_word[mark_j] not in [UNDETERMINED, NONE]:
				inflection_groups[i][inflection_j] = mark_word[mark_j]
			mark_j += 1

# returns a list of groupings of tuples that indicate a series of
# monosyllables composed of the given <active_inflections>, 
# where each tuple represents
# the index in the given <markup_clause> list
# and the subindex in the given <markup_clause> list.
def _find_series_of_monosyllables(markup_clause, active_inflections):
	monosyllable_series = [[]]
	for i, word in enumerate(markup_clause):
		current_series = monosyllable_series[-1];

		# searches for pure monosyllables.
		# if the <current_series> is empty or its last tuple
		# was a monosyllable that came directly before the current one,
		# then the current monosyllable is added to the <current_series>.
		# otherwise, the current monosyllable is the start of a new series.
		if len(word) == 1 and word[0] in active_inflections:
			if (
				len(current_series) == 0 
				or current_series[-1][0] == i - 1
			):
				current_series.append((i, 0)) # part of series
			else:
				monosyllable_series.append([(i, 0)]) # starts new series
			continue
		
		if len(word) <= 1:
			continue

		# searches for monosyllables isolated at the beginning/end of <word>.
		if (
			word[0] in active_inflections 
			and word[1] not in active_inflections
		):
			# monosyllable is isolated at the beginning of <word>.
			if len(current_series) == 0 or current_series[-1][0] == i - 1:
				current_series.append((i, 0)) # part of series
			else:
				monosyllable_series.append([(i, 0)]) # starts new series

		elif (
			word[-1] in active_inflections
			and word[-2] not in active_inflections
		):
			# monosyllable is isolated at the end of <word>.
			if len(current_series) == 0 or current_series[-1][0] == i - 1:
				current_series.append((i, len(word) - 1)) # part of series
			else:
				current_series.append([(i, len(word) - 1)]) # starts new series
	return monosyllable_series

def _is_neutral_inflection(inflection_num):
	return (
		inflection_num == _NEUTRAL_TONE_NUM
		or inflection_num in _TO_INFLECTED_NEUTRAL.values()
	)

def _print_markup_clause(rule_num, markup_clause, stay_inflection, to_inflection):
	MARK = {
		TO_INFLECTION["none"]:  "█",
		stay_inflection: "•",
		to_inflection: "^"
	}
	print(f"rule #{rule_num:>2d}:   ", end="")
	for i, word in enumerate(markup_clause):
		for j, mark in enumerate(word):
			print(MARK.get(mark, "x"), end="")
		if i + 1 < len(markup_clause):
			print("   ", end="")
	print("\n")
