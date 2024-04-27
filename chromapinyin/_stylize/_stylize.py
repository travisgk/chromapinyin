import math
from chromapinyin._syllable._punctuation_marks import (
	APOSTROPHES, CLAUSE_BREAKS, PUNCTUATION
)
from chromapinyin._syllable._vowel_chars import (
	APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM
)
from ._category_contents import *
from ._html_builder import embed_styling, HTML_line

def create_stylized_sentence(
	word_list,
	categories_2D,
	generate_css,
	vertical=False,
	exclude_punctuation=False,
	break_line_with_clauses=True,
	max_n_line_syllables=9
):
	reset_tabulation()
	word_lines = [[],]
	for word_i, word in enumerate(word_list):
		# embeds alignment to the syllable dictionaries.
		for syllable_i, syllable in enumerate(word):
			if len(word) > 1:
				if syllable_i == 0:
					word_list[word_i][syllable_i]["alignment"] = "start"
				elif syllable_i == len(word) - 1:
					word_list[word_i][syllable_i]["alignment"] = "end"
				else:
					word_list[word_i][syllable_i]["alignment"] = "center"
			else:
				word_list[word_i][syllable_i]["alignment"] = "center"

		if word[0]["hanzi"] in CLAUSE_BREAKS:
			# clause breaks are appended with its previous word,
			# so their own iterations are skipped.
			if break_line_with_clauses and word_i < len(word_list) - 1:
				word_lines.append([])
			continue

		# determines the number of syllables in the next word.
		n_apostrophes = len(
			[0 for syllable in word if syllable["pinyin"] in APOSTROPHES]
		)
		next_n_syllables = len(word) - n_apostrophes

		# adds an additional syllable if the next syllable is a clause break.
		next_word = (
			word_list[word_i + 1] if word_i + 1 < len(word_list) else None
		)
		next_word_is_clause_break = False
		if next_word and next_word[0]["hanzi"] in CLAUSE_BREAKS:
			next_n_syllables += len(word_list[word_i + 1])
			next_word_is_clause_break = True

		# determines how the number of syllables the current line will have
		# if the current <word> (and possibly a clause breaker) is added.
		# then, a new line is created if that number of syllables
		# exceeds the maximum amount of syllables per line.
		n_line_syllables = sum([len(word) for word in word_lines[-1]])
		prospective_n_line_syllables = n_line_syllables + next_n_syllables
		if prospective_n_line_syllables > max_n_line_syllables:
			word_lines.append([])

		# appends the current <word> (and possibly a clause breaker) 
		# to the current line.
		word_lines[-1].append(word)
		if next_word_is_clause_break:
			word_lines[-1].append(next_word)

	# breaks the <word_lines> into a 2D table of syllables.
	syllable_run = max(
		[sum([len(word) for word in line]) for line in word_lines]
	)
	n_lines = len(word_lines)
	n_cols = n_lines if vertical else syllable_run
	n_rows = syllable_run if vertical else n_lines
	syllable_table = [[None for _ in range(n_cols)] for _ in range(n_rows)]
	row, col = 0, 0
	if vertical:
		for line in word_lines:
			for word in line:
				for syllable in word:
					syllable_table[row][col] = syllable
					row += 1
			col += 1
			row = 0

	else:
		for line in word_lines:
			for word in line:
				for syllable in word:
					syllable_table[row][col] = syllable
					col += 1
			row += 1
			col = 0

	result = HTML_line(
		f"<table {embed_styling([CHROMA_TABLE], generate_css)}>", 1
	)
	css = ""

	for syllable_row in syllable_table:
		result += _return_syllable_row_HTML(
			syllable_row, categories_2D, generate_css, vertical
		)
	
	result += HTML_line("</table>", -1)

	return result, css

def _return_syllable_row_HTML(
	syllable_row, categories_2D, generate_css, vertical
):
	for row in categories_2D:
		print(row)
	syllable_cells_width = max([len(row) for row in categories_2D])
	syllable_cells_height = len(categories_2D)
	result = ""

	for categories_row in categories_2D:
		result += HTML_line(
			f"<tr {embed_styling([CHROMA_TR], generate_css)}>", 1
		)
		for syllable_i, syllable in enumerate(syllable_row):
			if not syllable or syllable["pinyin"] in APOSTROPHES:
				# skips None elements of the <syllable_row>
				# or elements that are solely a pinyin apostrophe.
				continue

			for category_i in range(syllable_cells_width):
				if category_i >= len(categories_row):
					print(f"{category_i} / {len(categories_row)}")
					result += HTML_line("<td></td>")
					continue

				category = categories_row[category_i]
				add_punct, return_blank = _return_additional_punctuation(
					syllable_row, category, syllable_i, generate_css
				)

				if return_blank:
					result += HTML_line("<td><!--additional_punct--></td>")
					continue

				result += _return_syllable_td_HTML(
					syllable, category, generate_css, vertical, add_punct
				)
		result += HTML_line("</tr>", -1)

	return result

def _return_additional_punctuation(
	syllable_row, category, syllable_i, generate_css
):
	category_is_tuple = isinstance(category, tuple)
	result = ""
	current_cell_is_blank = False
	if not category_is_tuple:
		# merging punctuation is not used,
		# so no additional punctuation is returned.
		return result, current_cell_is_blank

	category_name = category[0] if category_is_tuple else category
	PUNCTUATION_NUMS = [APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM]
	if category_name in ["pinyin", "ipa"] and "merge_punctuation" in category:
		inflection_num = syllable_row[syllable_i]["inflection_num"]
		if inflection_num in PUNCTUATION_NUMS:
			# merging punctuation is used,
			# but the current syllable is punctuation,
			# then the cell contents will be blank
			current_cell_is_blank = True
			return result, current_cell_is_blank
	else:
		# merging punctuation is not used.
		return result, current_cell_is_blank

	#
	if (
		syllable_i + 1 < len(syllable_row)
		and syllable_row[syllable_i + 1]
		and syllable_row[syllable_i + 1]["inflection_num"] in PUNCTUATION_NUMS
	):
		additional_punctuation = syllable_row[syllable_i + 1]["pinyin"]

		# a particular span is added around the punctuation.
		styling_classes = []
		if additional_punctuation in APOSTROPHES:
			# particular styling for an appended apostrophe is added.
			if "no_color" not in category:
				color_css = get_inflection_color_style(APOSTROPHE_TONE_NUM)
				styling_classes.append(color_css)
			styling_classes.append(CHROMA_APOSTROPHE_OFFSET)

		else:
			# styling for any other punctuation is added.
			if "no_color" not in category:
				color_css = get_inflection_color_style(PUNCTUATION_TONE_NUM)
				styling_classes.append(color_css)

		# additional punctuation HTML is created and returned.
		if len(styling_classes) > 0:
			styling = embed_styling(styling_classes, generate_css)
			result += f"<span {styling}>{additional_punctuation}</span>"
		else:
			result += additional_punctuation
	return result, current_cell_is_blank


def _return_syllable_td_HTML(
	syllable, category, generate_css, vertical, add_punct
):
	if category is None:
		return HTML_line("<td></td>")

	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	result = ""
	
	if category_name == "hanzi":
		result += return_hanzi_contents(
			syllable, category, generate_css, vertical
		)

	elif category_name == "pinyin":
		result += return_pinyin_contents(
			syllable, category, generate_css, vertical, add_punct
		)

	elif category_name == "zhuyin":
		result += return_zhuyin_contents(
			syllable, category, generate_css, vertical
		)

	elif category_name == "vertical_zhuyin":
		result += return_vertical_zhuyin_contents(
			syllable, category, generate_css, vertical
		)

	elif category_name == "ipa":
		result += return_ipa_contents(
			syllable, category, generate_css, vertical, add_punct
		)

	elif category_name == "pitch_graph":
		result += "" # return_pitch_graph_contents

	else:
		result += "<td></td>"

	return result