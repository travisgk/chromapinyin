import math
from ._inflection import TO_INFLECTION
from ._punctuation_marks import APOSTROPHES, CLAUSE_BREAKS, PUNCTUATION
from ._table_css import *
from ._vowel_chars import (
	_APOSTROPHE_TONE_NUM, _NONE_TONE_NUM, get_tone_num, strip_tone_marker
)
from .color_scheme import _CHROMA_TONES

_n_tabs = 0

def create_stylized_sentence(
	word_list,
	categories_2D,
	generate_css,
	vertical=False,
	grouped=True,
	exclude_punctuation=False,
	break_line_with_clauses=True,
	max_n_line_syllables=9
):
	global _n_tabs
	_n_tabs = 0

	word_lines = [[],]

	for word_i, word in enumerate(word_list):
		# embeds alignment to the syllable dictionaries.
		for syllable_i, syllable in enumerate(word):
			if grouped and len(word) > 1:
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

	result = _HTML_line(
		f"<table {_embed_styling([_CHROMA_TABLE], generate_css)}>", 1
	)
	css = ""

	for syllable_row in syllable_table:
		result += _return_syllable_row_HTML(
			syllable_row, categories_2D, generate_css, vertical
		)
	
	result += _HTML_line("</table>", -1)

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
		result += _HTML_line(
			f"<tr {_embed_styling([_CHROMA_TR], generate_css)}>", 1
		)
		for syllable_i, syllable in enumerate(syllable_row):
			if not syllable or syllable["pinyin"] in APOSTROPHES:
				# skips None elements of the <syllable_row>
				# or elements that are solely a pinyin apostrophe.
				continue

			for category_i in range(syllable_cells_width):
				if category_i >= len(categories_row):
					print(f"{category_i} / {len(categories_row)}")
					result += _HTML_line("<td></td>")
					continue

				category = categories_row[category_i]
				add_punct, return_blank = _return_additional_punctuation(
					syllable_row, category, syllable_i, generate_css
				)

				if return_blank:
					result += _HTML_line("<td><!--additional_punct--></td>")
					continue

				result += _return_syllable_td_HTML(
					syllable, category, generate_css, vertical, add_punct
				)
		result += _HTML_line("</tr>", -1)

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
	PUNCTUATION_NUMS = [_APOSTROPHE_TONE_NUM, _NONE_TONE_NUM]
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
			if "no_color" not in category:
				color_css = _CHROMA_TONES[TO_INFLECTION["apostrophe"]]
				styling_classes.append(color_css)
			styling_classes.append(_CHROMA_APOSTROPHE_OFFSET)

		else:
			if "no_color" not in category:
				color_css = _CHROMA_TONES[TO_INFLECTION["none"]]
				styling_classes.append(color_css)

		if len(styling_classes) > 0:
			styling = _embed_styling(styling_classes, generate_css)
			result += f"<span {styling}>{additional_punctuation}</span>"
		else:
			result += additional_punctuation
	return result, current_cell_is_blank


def _return_syllable_td_HTML(
	syllable, category, generate_css, vertical, add_punct
):
	if category is None:
		return _HTML_line("<td></td>")

	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	result = ""
	
	if category_name == "hanzi":
		result += _return_hanzi_contents(
			syllable, category, generate_css, vertical
		)

	elif category_name == "pinyin":
		result += _return_pinyin_contents(
			syllable, category, generate_css, vertical, add_punct
		)

	elif category_name == "zhuyin":
		result += _return_zhuyin_contents(
			syllable, category, generate_css, vertical
		)

	elif category_name == "vertical_zhuyin":
		result += _return_vertical_zhuyin_contents(
			syllable, category, generate_css, vertical
		)

	elif category_name == "ipa":
		result += _return_ipa_contents(
			syllable, category, generate_css, vertical, add_punct
		)

	elif category_name == "pitch_chart":
		result += ""

	else:
		result += "<td></td>"

	return result

def _return_hanzi_contents(syllable, category, generate_css, vertical):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	alignment = syllable["alignment"]

	# opens the <td> element.
	td_styling_classes = [_CATEGORY_TO_TD_STYLE[category_name],]
	if vertical:
		td_styling_classes.append(_return_td_align_style(alignment, vertical))
	td_styling = _embed_styling(td_styling_classes, generate_css)
	result = _HTML_line(f"<td {td_styling}>", 1)

	# opens the <div> container element.
	div_styling_classes = [_CHROMA_DIV_HANZI_CONTAINER,]
	if not vertical:
		div_styling_classes.append(_return_div_h_align_style(alignment))
	div_styling = _embed_styling(div_styling_classes, generate_css)
	result += _HTML_line(f"<div {div_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = _CHROMA_TONES[syllable["inflection_num"]]
	span_styling_classes = [color_css, _CHROMA_HANZI_OFFSET,]
	span_styling = _embed_styling(span_styling_classes, generate_css)
	hanzi = syllable["hanzi"]
	result += _HTML_line(f"<span {span_styling}>{hanzi}</span>")

	# closes elements.
	result += _HTML_line("</div>", -1)
	result += _HTML_line("</td>", -1)

	return result

def _return_pinyin_contents(
	syllable, category, generate_css, vertical, add_punct
):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	alignment = syllable["alignment"]

	# opens the <td> element.
	td_styling_classes = [_CATEGORY_TO_TD_STYLE[category_name],]
	td_styling_classes.append(_return_td_align_style(alignment, vertical))
	td_styling = _embed_styling(td_styling_classes, generate_css)
	result = _HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = _CHROMA_TONES[syllable["inflection_num"]]
	span_styling = _embed_styling([color_css,], generate_css)
	pinyin = syllable["pinyin"]
	result += _HTML_line(f"<span {span_styling}>{pinyin}</span>" + add_punct)

	# closes elements.
	result += _HTML_line("</td>", -1)

	return result

def _return_zhuyin_contents(syllable, category, generate_css, vertical):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	alignment = syllable["alignment"]

	# opens the <td> element.
	td_styling_classes = [_CATEGORY_TO_TD_STYLE[category_name],]
	td_styling_classes.append(_return_td_align_style(alignment, vertical))
	td_styling = _embed_styling(td_styling_classes, generate_css)
	result = _HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	span_line = ""
	color_css = _CHROMA_TONES[syllable["inflection_num"]]
	span_styling = _embed_styling([color_css,], generate_css)
	span_line += f"<span {span_styling}>"

	prefix = syllable["zhuyin_prefix"]
	if len(prefix) > 0:
		span_styling = _embed_styling([_CHROMA_ZHUYIN_PREFIX,], generate_css)
		span_line += f"<span {span_styling}>{prefix}</span>"
	
	root = syllable["zhuyin_root"]
	span_styling = _embed_styling([_CHROMA_ZHUYIN_ROOT,], generate_css)
	span_line += f"<span {span_styling}>{root}</span>"

	suffix = syllable["zhuyin_suffix"]
	if len(suffix) > 0:
		span_styling = _embed_styling([_CHROMA_ZHUYIN_SUFFIX,], generate_css)
		span_line += f"<span {span_styling}>{suffix}</span>"
	
	span_line += "</span>"

	result += _HTML_line(span_line)

	# closes elements.
	result += _HTML_line("</td>", -1)

	return result

def _return_vertical_zhuyin_contents(
	syllable, category, generate_css, vertical
):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	alignment = syllable["alignment"]

	# opens the <td> element.
	td_styling_classes = [_CATEGORY_TO_TD_STYLE[category_name],]
	if vertical:
		td_styling_classes.append(_return_td_align_style(alignment, vertical))
	td_styling = _embed_styling(td_styling_classes, generate_css)
	result = _HTML_line(f"<td {td_styling}>", 1)

	# opens the <div> container element.
	div_styling = _embed_styling([_CHROMA_DIV_ZHUYIN_CONTAINER,], generate_css)
	result += _HTML_line(f"<div {div_styling}>", 1)

	# opens the nested <table> element.
	table_styling = _embed_styling([_CHROMA_TABLE,], generate_css)
	result += _HTML_line(f"<table {table_styling}>", 1)

	# opens the nested <tr> and <td> elements.
	nested_styling = _embed_styling([_CHROMA_NESTED_ZHUYIN], generate_css)
	result += _HTML_line(f"<tr {nested_styling}>", 1)

	# creates the spans for the prefix and root.
	result += _HTML_line(f"<td {nested_styling}>", 1)
	
	color_css = _CHROMA_TONES[syllable["inflection_num"]]
	color_styling = _embed_styling([color_css,], generate_css)
	result += _HTML_line(f"<div {color_styling}>", 1)

	span_line = ""
	prefix = syllable["zhuyin_prefix"]
	if len(prefix) > 0:
		span_styling = _embed_styling(
			[_CHROMA_ZHUYIN_PREFIX, _CHROMA_ZHUYIN_PREFIX_OFFSET,], generate_css
		)
		span_line += f"<span {span_styling}>{prefix}</span>"

	root = syllable["zhuyin_root"]
	span_styling = _embed_styling(
		[_CHROMA_ZHUYIN_ROOT, _CHROMA_VERTICAL_ZHUYIN], generate_css
	)
	span_line += f"<span {span_styling}>{root}</span>"

	result += _HTML_line(span_line)
	result += _HTML_line("</div>", -1)
	result += _HTML_line("</td>", -1)

	# creates the spans for the suffix.
	result += _HTML_line(f"<td {nested_styling}>", 1)
	result += _HTML_line(f"<div {color_styling}>", 1)

	span_line = ""
	suffix = syllable["zhuyin_suffix"]
	span_styling = _embed_styling(
		[_CHROMA_ZHUYIN_SUFFIX, _CHROMA_ZHUYIN_SUFFIX_OFFSET,], generate_css
	)
	span_line += f"<span {span_styling}>{suffix}</span>"

	result += _HTML_line(span_line)
	result += _HTML_line("</div>", -1)
	result += _HTML_line("</td>", -1)

	# closes the rest of the elements.
	result += _HTML_line("</tr>", -1)
	result += _HTML_line("</table>", -1)
	result += _HTML_line("</div>", -1)
	result += _HTML_line("</td>", -1)

	return result

def _return_ipa_contents(
	syllable, category, generate_css, vertical, add_punct
):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	alignment = syllable["alignment"]

	# opens the <td> element.
	td_styling_classes = [_CATEGORY_TO_TD_STYLE[category_name],]
	td_styling_classes.append(_return_td_align_style(alignment, vertical))
	td_styling = _embed_styling(td_styling_classes, generate_css)
	result = _HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = _CHROMA_TONES[syllable["inflection_num"]]
	span_styling = _embed_styling([color_css,], generate_css)
	ipa_root = syllable["ipa_root"]
	ipa_suffix = syllable["ipa_suffix"]
	ipa = ipa_root + ipa_suffix
	result += _HTML_line(f"<span {span_styling}>{ipa}</span>" + add_punct)

	# closes elements.
	result += _HTML_line("</td>", -1)

	return result

def _return_td_align_style(alignment, vertical):
	if alignment == "start":
		return _CHROMA_TD_ALIGN_BOTTOM if vertical else _CHROMA_TD_ALIGN_RIGHT
	elif alignment == "end":
		return _CHROMA_TD_ALIGN_TOP if vertical else _CHROMA_TD_ALIGN_LEFT
	else:
		return _CHROMA_TD_ALIGN_CENTER # UNCERTAIN

def _return_div_h_align_style(alignment):
	if alignment == "start":
		return _CHROMA_DIV_PUSH_RIGHT
	elif alignment == "end":
		return _CHROMA_DIV_PUSH_LEFT
	else:
		return _CHROMA_DIV_PUSH_CENTER # UNCERTAIN

# returns the text that goes after an HTML tag declaration
# to indicate that tag's styling.
def _embed_styling(style_dicts, uses_css):
	if uses_css:
		class_names = " ".join(
			[style_dict["class"].split(".")[-1] for style_dict in style_dicts]
		)
		return f"class=\"{class_names}\""

	return (
		"style=\"" 
		+ " ".join([
			"".join(style_line.replace('"', '').split()) 
			for style_dict in style_dicts 
			for style_line in style_dict["style"]]
		) 
		+ "\""
	)

# returns a string of HTML formatting with the current tabulation applied.
# <tab_inc> will increase/decrease the current tabulation after/before
# the given <HTML> line depending on 
# if <tab_inc> is positive/negative respectively.
def _HTML_line(HTML, tab_inc=0):
	global _n_tabs
	if tab_inc < 0:
		_n_tabs += tab_inc
		result = "\t" * _n_tabs + HTML + "\n"

	elif tab_inc > 0:
		result = "\t" * _n_tabs + HTML + "\n"
		_n_tabs += tab_inc

	else:
		result = "\t" * _n_tabs + HTML + "\n"
	return result
