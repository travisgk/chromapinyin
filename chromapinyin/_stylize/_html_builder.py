# chromapinyin._stylize._html_builder.py
# ---
# this file contains the primary function that returns an HTML table
# of chinese with stylized tone colors when given:
# 	- a <word_list> from create_word_list(...) (chromapinyin._words._word_list.py).
# 	- a 2D list of categories.
# 	- the option to generate CSS.
#
# ---
# each sublist of <categories_2D> will be a row of components for *each* syllable.
# within these sublists, category components are defined.
# an element will either be a single string that indicates the category name,
# or it will be a tuple that has its first element being the category name
# and uses its other elements to provide additional formatting information.
#
# categories that can be used are:
# 	- "hanzi": the syllable's hanzi character.
# 	- "pinyin": the syllable's pinyin character.
# 	- "zhuyin": the syllable's zhuyin transcription.
# 	- "vertical_zhuyin": the syllable's zhuyin transcription rendered vertically.
# 	- "ipa": the syllable's international phonetic alphabet transcription.
# 	- "pitch_graph": the path to an image representing the syllable's spoken tone.
#   - "blank": an empty table cell. used to block cell merging.
#
# additional formatting can be provided when the element is a tuple,
# like ("pinyin", "grouped", "split_punctuation").
# these additional settings are:
# 	- "grouped": this category's cells for syllables belonging to the same word
# 	             will be aligned so that they're squished together.
#	- "split_punctuation": punctuation in this category's cells won't be merged
# 	                       with the cell to its right. only applicable for
# 	                       pinyin or ipa.
#	- "number_tones": the tones of pinyin, zhuyin, or ipa 
# 	                  will be expressed with a number.
# 	                  pinyin will use the innate tone,
# 	                  while zhuyin and ipa will use the spoken tone.
# 	- "no_tones": the tones of pinyin, zhuyin, or ipa will not be included.
# 	- "no_color": coloring spans will not be used.
#   - "manual_night_mode": this is used if the user wants night mode styling
#	                      embedded inline for their GIFs, since without CSS
#	                      these stylings can't be reached.
#

import math
from chromapinyin._syllable._punctuation_marks import (
	APOSTROPHES, CLAUSE_BREAKS, PUNCTUATION
)
from chromapinyin._syllable._vowel_chars import (
	APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM
)
from ._category_contents import *
from ._color_scheme import (
	get_chroma_tone_values,
	get_chroma_gif_colors_white_values,
	get_chroma_gif_colors_black_values
)
from ._formatting_helper import (
	reset_tabulation, embed_styling, HTML_line, colspan_str
)

# returns an HTML table of stylized chinese syllables.
def create_stylized_sentence(
	word_list,
	categories_2D,
	use_css,
	use_colspan=True,
	vertical=False,
	break_line_with_clauses=True,
	hide_clause_breaks=False,
	max_n_line_syllables=99
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

		# determines the number of syllables in the current word
		# and if the next "word" is a clause break.
		n_apostrophes = len(
			[0 for syllable in word if syllable["pinyin"] in APOSTROPHES]
		)
		n_new_syllables = len(word) - n_apostrophes
		next_word = (
			word_list[word_i + 1] if word_i + 1 < len(word_list) else None
		)
		next_word_is_clause_break = False
		if next_word and next_word[0]["hanzi"] in CLAUSE_BREAKS:
			n_new_syllables += (
				0 if hide_clause_breaks else len(word_list[word_i + 1])
			)
			next_word_is_clause_break = True

		# determines how the number of syllables the current line will have
		# if the current <word> (and possibly a clause breaker) is added.
		# then, a new line is created if that number of syllables
		# added on to the current line
		# exceeds the maximum amount of syllables per line.
		n_line_syllables = sum([len(word) for word in word_lines[-1]])
		prospective_n_line_syllables = n_line_syllables + n_new_syllables
		if prospective_n_line_syllables > max_n_line_syllables:
			word_lines.append([])

		# appends the current <word> (and possibly a clause breaker) 
		# to the current line.
		word_lines[-1].append(word)
		if next_word_is_clause_break:
			word_lines[-1].append(next_word)

	# breaks the <word_lines> into a 2D table of syllables.
	syllable_run = max(
		[
			sum(
				[
					len(word) for word in line
					if not hide_clause_breaks
					or word[0]["hanzi"] not in CLAUSE_BREAKS
				]
			) for line in word_lines
		]
	)
	n_lines = len(word_lines)
	n_cols = n_lines if vertical else syllable_run
	n_rows = syllable_run if vertical else n_lines
	syllable_table = [[None for _ in range(n_cols)] for _ in range(n_rows)]
	
	# copies syllables to their respective position in the table.
	row, col = 0, 0
	if vertical:
		for line in word_lines:
			for word in line:
				for syllable in word:
					if hide_clause_breaks and syllable["hanzi"] in CLAUSE_BREAKS:
						continue
					syllable_table[row][col] = syllable
					row += 1
			col += 1
			row = 0

	else:
		for line in word_lines:
			for word in line:
				for syllable in word:
					if hide_clause_breaks and syllable["hanzi"] in CLAUSE_BREAKS:
						continue
					syllable_table[row][col] = syllable
					col += 1
			row += 1
			col = 0

	# builds the HTML.
	result = HTML_line(
		f"<table {embed_styling([CHROMA_TABLE], use_css)}>", 1
	)
	for syllable_row in syllable_table:
		result += _return_syllable_row_HTML(
			syllable_row, categories_2D, use_css, use_colspan, vertical
		)
	result += HTML_line("</table>", -1)
	return result

# returns the CSS for all the utilized classes.
def generate_CSS():
	reset_tabulation()
	css = ""
	style_sections = []
	style_sections.append(
		(	
			"TABLE",
			(
				CHROMA_DIV_PUSH_LEFT,
				CHROMA_DIV_PUSH_RIGHT,
				CHROMA_DIV_PUSH_CENTER,
				CHROMA_TD_ALIGN_CENTER,
				CHROMA_TD_ALIGN_TOP,
				CHROMA_TD_ALIGN_RIGHT,
				CHROMA_TD_ALIGN_BOTTOM,
				CHROMA_TD_ALIGN_LEFT,
				CHROMA_TABLE,
				CHROMA_TABLE_NESTED,
				CHROMA_TR,
				CHROMA_TD,
			),
		)
	)


	style_sections.append(
		(
			"HANZI",
			(
				get_content_style("CHROMA_TD_HANZI"),
				get_content_style("CHROMA_HANZI_OFFSET"),
				get_content_style("CHROMA_DIV_HANZI_CONTAINER"),
			),
		)
	)

	style_sections.append(
		(
			"PINYIN",
			(
				get_content_style("CHROMA_TD_PINYIN"),
				CHROMA_APOSTROPHE_OFFSET,
			),
		)
	)

	style_sections.append(
		(
			"ZHUYIN",
			(
				CHROMA_TD_ZHUYIN,
				get_content_style("CHROMA_ZHUYIN_PREFIX"),
				get_content_style("CHROMA_ZHUYIN_ROOT"),
				get_content_style("CHROMA_ZHUYIN_SUFFIX"),
				get_content_style("CHROMA_INLINE_ZHUYIN"),
				get_content_style("CHROMA_VERTICAL_ZHUYIN"),
				CHROMA_DIV_ZHUYIN_CONTAINER,
				CHROMA_NESTED_ZHUYIN,
				CHROMA_VERTICAL_ZHUYIN_PREFIX_OFFSET,
				CHROMA_ZHUYIN_PREFIX_CONTAINER,
				CHROMA_ZHUYIN_SUFFIX_OFFSET,
				CHROMA_ZHUYIN_SUFFIX_CONTAINER,
			),
		)
	)

	style_sections.append(
		(
			"PITCH_GRAPH",
			(
				CHROMA_TD_PITCH_GRAPH,
				get_content_style("CHROMA_IMG_PITCH_GRAPH"),
			),
		)
	)

	style_sections.append(
		(
			"HANDWRITING",
			(
				CHROMA_TD_HANDWRITING,
				get_content_style("CHROMA_IMG_HANDWRITING"),
			),
		)
	)

	style_sections.append(("tone colors", get_chroma_tone_values(),))
	style_sections.append(
		("GIF white filters", get_chroma_gif_colors_white_values(),)
	)
	style_sections.append(
		("GIF black filters", get_chroma_gif_colors_black_values(),)
	)

	for style_section in style_sections:
		css += f"\n/* {style_section[0]} */\n"
		for style_dict in style_section[1]:
			css += _return_CSS(style_dict) + "\n"
	return css

# returns a string that contains the given <style_dict> formatted for CSS.
def _return_CSS(style_dict):
	class_str = style_dict["class"]
	if "." not in class_str:
		class_str = "." + class_str
	css = class_str + " {\n"
	lines = style_dict["style"]
	for line in lines:
		css += f"\t{line}\n"
	css += "}\n"
	return css

# returns a string that contains a row of contents in the HTML table.
def _return_syllable_row_HTML(
	syllable_row, categories_2D, use_css, use_colspan, vertical
):
	syllable_cells_width = max([len(row) for row in categories_2D])
	syllable_cells_height = len(categories_2D)
	result = ""

	for categories_row in categories_2D:
		result += HTML_line(
			f"<tr {embed_styling([CHROMA_TR], use_css)}>", 1
		)
		for syllable_i, syllable in enumerate(syllable_row):
			if not syllable:
				# blank cells are inserted to align words
				# that have had word-wrapping applied.
				if not use_colspan:
					for category_i in range(syllable_cells_width):
						result += HTML_line("<td></td>")
				continue

			if syllable["pinyin"] in APOSTROPHES:
				# skips None elements of the <syllable_row>
				# or elements that are solely a pinyin apostrophe.
				continue

			for category_i in range(syllable_cells_width):
				if category_i >= len(categories_row):
					if not use_colspan:
						result += HTML_line("<td></td>")
					continue

				category = categories_row[category_i]
				add_punct, return_blank = _return_additional_punctuation(
					syllable_row, category, syllable_i, use_css
				)

				if return_blank:
					# blank <td> that lacks punctuation because its
					# punctuation was merged to the right.
					result += HTML_line("<td></td>")
					continue

				result += _return_syllable_td_HTML(
					syllable,
					categories_row,
					category_i,
					use_css,
					use_colspan,
					syllable_cells_width,
					vertical,
					add_punct
				)
		result += HTML_line("</tr>", -1)

	return result

# returns HTML that's appended to the current cell's contents.
# this is used to move isolated punctuation from its
# own cell into the cell to its right.
# an additional boolean is returned,
#
def _return_additional_punctuation(
	syllable_row, category, syllable_i, use_css
):
	category_is_tuple = isinstance(category, tuple)
	result = ""
	current_cell_is_blank = False
	if category_is_tuple and "split_punctuation" in category:
		# merging punctuation is not used,
		# so no additional punctuation is returned.
		return result, current_cell_is_blank

	category_name = category[0] if category_is_tuple else category
	PUNCTUATION_NUMS = [APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM]
	if category_name in ["pinyin", "ipa"]:
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
			styling = embed_styling(styling_classes, use_css)
			result += f"<span {styling}>{additional_punctuation}</span>"
		else:
			result += additional_punctuation
	return result, current_cell_is_blank

# returns the HTML that defines a table cell element
# containing the appropriate syllable information.
def _return_syllable_td_HTML(
	syllable,
	categories_row,
	category_i,
	use_css,
	use_colspan,
	syllable_cells_width,
	vertical,
	add_punct
):
	category = categories_row[category_i]
	if category is None:
		if not use_colspan:
			return HTML_line("<td></td>")
		return ""

	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	result = ""
	
	colspan = 1
	if use_colspan:
		for i in range(category_i + 1, syllable_cells_width):
			if (
				i >= len(categories_row) 
				or (i < len(categories_row) and categories_row[i] == None)
			):
				colspan += 1
			elif i < len(categories_row) and categories_row[i] != None:
				break

	if category_name == "hanzi":
		result += return_hanzi_contents(
			syllable, category, use_css, colspan, vertical
		)

	elif category_name == "pinyin":
		result += return_pinyin_contents(
			syllable, category, use_css, colspan, vertical, add_punct
		)

	elif category_name == "zhuyin":
		result += return_zhuyin_contents(
			syllable, category, use_css, colspan, vertical, vertical_zhuyin=False
		)

	elif category_name == "vertical_zhuyin":
		result += return_zhuyin_contents(
			syllable, category, use_css, colspan, vertical, vertical_zhuyin=True
		)

	elif category_name == "ipa":
		result += return_ipa_contents(
			syllable, category, use_css, colspan, vertical, add_punct
		)

	elif category_name == "pitch_graph":
		result += return_pitch_graph_contents(
			syllable, category, use_css, colspan, vertical
		)

	elif category_name == "handwriting":
		result += return_handwriting_contents(
			syllable, category, use_css, colspan, vertical
		)

	elif category_name == "blank":
		result += HTML_line(f"<td {colspan_str(colspan)}></td>")

	elif not use_colspan:
		result += HTML_line(f"<td></td>")

	return result