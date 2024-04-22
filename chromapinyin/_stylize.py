from ._inflection import TO_INFLECTION
from ._punctuation_marks import PUNCTUATION
from ._vowel_chars import _NEUTRAL_TONE_NUM, get_tone_num, strip_tone_marker
from ._table_css import *
from .color_scheme import _CHROMA_TONES

# takes a source syllable list
#
# takes a list of table categories: "hanzi", "hanzi_with_vertical_zhuyin", "pinyin", "pinyin_with_nums", "pinyin_no_tones", "ipa", "zhuyin", "vertical_zhuyin", "pitch_chart"
# if given as a tuple, "group_punctuation" is an additional option that can be included,
# as well as "no_color", "color_by_tone", "color_by_spoken_tone", "color_by_inflection".
# "exclude_punctuation" will be ignored for "hanzi", "hanzi_with_vertical_zhuyin", and "zhuyin".
#
# takes a bool to determine if the table should be rendered horizontally or vertically.
#
# takes a bool to determine if "word" units should be grouped together by aligning.
#
# takes a bool to determine if stylings should be given in CSS or put inline
#

# returns a list of groupings (lists) of dictionary objects.
# each dictionary object represents a syllable,
# which has the keys as defined in chromapinyin.inflection.py:
#
# "hanzi": the syllable written in hanzi.
# "pinyin": the syllable written in pinyin.
# "ipa": the syllable transcribed in the international phonetic alphabet.
# "zhuyin": the syllable transcribed in zhuyin.

_n_tabs = 0

# returns the <html_table> and the <css> as a tuple.
def create_stylized_sentence(
	syllable_list,
	categories,
	generate_css,
	vertical=False,
	grouped=True,
	exclude_punctuation=False
):
	global _n_tabs
	_n_tabs = 0
	html_table = _HTML_line(
		f"<table {_embed_styling([_CHROMA_TABLE], generate_css)}>"
	)
	_n_tabs += 1
	css = ""
	
	if vertical:
		for i, word in enumerate(syllable_list):
			for j, syllable in enumerate(word):
				html_table += _HTML_line("<tr>")
				_n_tabs = 2
				
				if (
					exclude_punctuation 
					and syllable["inflection_num"] == TO_INFLECTION["none"]
				):
					continue

				for category in categories:
					html_table += _return_td(
						syllable_list,
						category,
						i,
						j,
						generate_css,
						vertical,
						grouped
					)

				_n_tabs = 1
				html_table += _HTML_line("</tr>")

	else:
		for category in categories:
			html_table += _HTML_line("<tr>")
			_n_tabs = 2

			for i, word in enumerate(syllable_list):
				for j, syllable in enumerate(word):
					if (
						exclude_punctuation 
						and syllable["inflection_num"] == TO_INFLECTION["none"]
					):
						continue

					html_table += _return_td(
						syllable_list,
						category,
						i,
						j,
						generate_css,
						vertical,
						grouped
					)

			_n_tabs = 1
			html_table += _HTML_line("</tr>")

	html_table += _HTML_line("</table>", -1)

	print(html_table)
	print(css)
	return html_table, css

# returns the HTML representing a table cell as a <td> element.
def _return_td(
	syllable_list,
	category,
	i,
	j,
	generate_css,
	vertical,
	grouped
):
	global _n_tabs
	result = ""
	word = syllable_list[i]
	syllable = word[j]
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	style_classes = [_CHROMA_TD, _CATEGORY_TO_TD_STYLE[category_name]]

	# adds an aligning styling to push groups together.
	if grouped and len(word) > 1:
		if j == 0:
			style_classes.append(
				_CHROMA_BOTTOM_ALIGN if vertical else _CHROMA_RIGHT_ALIGN
			)
		elif j == len(word) - 1:
			style_classes.append(
				_CHROMA_TOP_ALIGN if vertical else _CHROMA_LEFT_ALIGN
			)

	styling = _embed_styling(style_classes, generate_css)
	
	result += _HTML_line(f"<td {styling}>", 1)

	# gets the HTML to go inside the <td>.
	result += _return_cell_contents(
		syllable_list,
		category,
		category_is_tuple,
		i,
		j,
		generate_css,
		vertical,
		grouped
	)

	# closes all tags and returns the complete <td>...</td> element.
	result += _HTML_line("</td>", -1)
	return result

# returns the HTML that goes inside a <td> element.
def _return_cell_contents(
	syllable_list,
	category,
	category_is_tuple,
	i,
	j,
	generate_css,
	vertical,
	grouped
):
	category_name = category[0] if category_is_tuple else category
	syllable = syllable_list[i][j]
	additional_punctuation = ""
	
	additional_punctuation, return_blank = _return_additional_punctuation(
		syllable_list, category, category_is_tuple, i, j, generate_css
	)
	if return_blank:
		return ""
	
	global _n_tabs
	result = ""

	# determines color styling by tone.
	# by default the syllables are colored by inflection.
	color_css = None
	if category_is_tuple:
		if "color_by_tone" in category:
			color_css = _CHROMA_TONES[syllable["tone_num"]]
		elif "color_by_spoken_tone" in category:
			color_css = _CHROMA_TONES[syllable["spoken_tone_num"]]
		elif "no_color" not in category:
			color_css = _CHROMA_TONES[syllable["inflection_num"]]
	else:
		color_css = _CHROMA_TONES[syllable["inflection_num"]]
		p = syllable["pinyin"]
		inf = syllable["inflection_num"]

	# opens a span that gives the text contents color.
	if color_css:
		styling = _embed_styling([color_css], generate_css)
		result += _HTML_line(f"<span {styling}>", 1)

	# returns the formatted hanzi immediately
	if category_name == "hanzi":
		result += _HTML_line(syllable["hanzi"])
		result += _HTML_line("</span>", -1)
		return result

	if category_name == "pinyin":
		pinyin_str = ""
		if category_is_tuple:
			if "with_nums" in category:
				pinyin_str += strip_tone_marker(syllable["pinyin"])
				if syllable["tone_num"] != _NEUTRAL_TONE_NUM:
					pinyin_str += str(syllable["tone_num"])
			elif "no_tones" in category:
				pinyin_str += strip_tone_marker(syllable["pinyin"])
			else:
				pinyin_str += syllable["pinyin"]
		else:
			pinyin_str += syllable["pinyin"]
		result += _HTML_line(pinyin_str + additional_punctuation)
		
	elif category_name == "ipa":
		ipa_str = ""
		if category_is_tuple:
			if "with_nums" in category:
				ipa_str += syllable["ipa_root"]
				if syllable["tone_num"] != _NEUTRAL_TONE_NUM:
					ipa_str += str(syllable["tone_num"])
			elif "no_tones" in category:
				ipa_str += syllable["ipa_root"]
			else:
				ipa_str += syllable["ipa"]
		else:
			ipa_str = syllable["ipa"]
		result += _HTML_line(ipa_str + additional_punctuation)

	elif category_name == "zhuyin":
		zhuyin_str = ""
		if category_is_tuple:
			if "with_nums" in category:
				zhuyin_str += syllable["zhuyin_root"]
				if syllable["tone_num"] != _NEUTRAL_TONE_NUM:
					zhuyin_str += str(syllable["tone_num"])
			elif "no_tones" in category:
				zhuyin_str += syllable["zhuyin_root"]
		else:
			zhuyin_str += syllable["zhuyin"]
		result += _HTML_line(zhuyin_str)

	elif category_name == "vertical_zhuyin":
		result += _return_vertical_zhuyin_table(
			syllable_list,
			category,
			category_is_tuple,
			i,
			j,
			generate_css,
			grouped,
			include_hanzi=False
		)

	elif category_name == "hanzi_with_zhuyin":
		result += _return_vertical_zhuyin_table(
			syllable_list,
			category,
			category_is_tuple,
			i,
			j,
			generate_css,
			grouped,
			include_hanzi=True
		)

	# closes color span.
	if color_css:
		result += _HTML_line("</span>", -1)

	#
	return result

# returns the HTML for a complete nested <table>
# that displays vertical zhuyin, with the option
# to include the corresponding hanzi to the right of it.
def _return_vertical_zhuyin_table(
	syllable_list,
	category,
	category_is_tuple,
	i,
	j,
	generate_css,
	grouped,
	include_hanzi
):
	global _n_tabs
	syllable = syllable_list[i][j]
	styling = _embed_styling([_CHROMA_VERTICAL_ZHUYIN_TABLE], generate_css)
	result = _HTML_line(f"<table {styling}>", 1)
	result += _HTML_line("<tr>", 1)
	half_pad_styling = _embed_styling([_CHROMA_HALF_PAD], generate_css)

	if grouped and len(syllable_list[i]) > 1:
		# a grouped polysyllable may need aligning.
		if j == 0:
			# a full padding <td> is inserted on the left.
			styling = _embed_styling([_CHROMA_FULL_PAD], generate_css)
			result += _HTML_line(f"<td {styling}></td>")

		elif not j == len(syllable_list[i]) - 1:
			# a half padding <td> is inserted on the left.
			styling = _embed_styling([_CHROMA_HALF_PAD], generate_css)
			result += _HTML_line(f"<td {styling}></td>")

		# gets cell contents and styling.
		zhuyin_no_mark = (
			syllable["zhuyin_prefix"] + syllable["zhuyin_root"]
		).strip()
		zhuyin_mark = syllable["zhuyin_suffix"]

		class_styling = _embed_styling(
			[_CHROMA_VERTICAL_ZHUYIN_ROOT], generate_css
		)
		span_styling = _embed_styling(
			[_CHROMA_VERTICAL_TEXT], generate_css
		)
		mark_styling = _embed_styling(
			[
				_CHROMA_VERTICAL_SINGLE_ZHUYIN_MARKER
				if len(zhuyin_no_mark) == 1
				else _CHROMA_VERTICAL_MULTI_ZHUYIN_MARKER
			],
			generate_css
		)
		
		# adds the primary content cells to the nested table.
		if include_hanzi:
			td_styling = _embed_styling(
				[_CHROMA_ZHUYIN_BY_HANZI_TD], generate_css
			)
			table_styling = _embed_styling(
				[_CHROMA_NESTED_VERTICAL_ZHUYIN_TABLE], generate_css
			)
			hanzi = syllable["hanzi"]
			result += _HTML_line(f"<td>{hanzi}</td>")
			result += _HTML_line(f"<td {td_styling}>", 1)
			result += _HTML_line(f"<table {table_styling}>", 1)
			result += _HTML_line(f"<tr><td {half_pad_styling}></td></tr>")
			result += _HTML_line("<tr>", 1)

		result += _HTML_line(f"<td {class_styling}>", 1)
		result += _HTML_line(f"<span {span_styling}>", 1)
		result += _HTML_line(f"{zhuyin_no_mark}")
		result += _HTML_line("</span>", -1)
		result += _HTML_line("</td>", -1)
		result += _HTML_line(f"<td {mark_styling}>{zhuyin_mark}</td>")

		# closes embedded hanzi table.
		if include_hanzi:
			result += _HTML_line("</tr>", -1)
			result += _HTML_line(f"<tr><td {half_pad_styling}></td></tr>")
			result += _HTML_line("</table>", -1)
			result += _HTML_line("</td>", -1)

		if j == len(syllable_list[i]) - 1:
			# a full padding <td> is inserted on the right.
			styling = _embed_styling([_CHROMA_FULL_PAD], generate_css)
			result += _HTML_line(f"<td {styling}></td>")

		elif not j == 0:
			# a half padding <td> is inserted on the right.
			result += _HTML_line(f"<td {half_pad_styling}></td>")
		
	else:
		# half-padding <td>s are inserted on both sides to align center.
		# gets cell contents and styling.
		zhuyin_no_mark = (
			syllable["zhuyin_prefix"] + syllable["zhuyin_root"]
		).strip()
		zhuyin_mark = syllable["zhuyin_suffix"]

		class_styling = _embed_styling(
			[_CHROMA_VERTICAL_ZHUYIN_ROOT], generate_css
		)
		span_styling = _embed_styling(
			[_CHROMA_VERTICAL_TEXT], generate_css
		)
		mark_styling = _embed_styling(
			[
				_CHROMA_VERTICAL_SINGLE_ZHUYIN_MARKER
				if len(zhuyin_no_mark) == 1
				else _CHROMA_VERTICAL_MULTI_ZHUYIN_MARKER
			],
			generate_css
		)
		result += _HTML_line(f"<td {half_pad_styling}></td>")

		# adds the primary content cells to the nested table.
		if include_hanzi:
			td_styling = _embed_styling(
				[_CHROMA_ZHUYIN_BY_HANZI_TD], generate_css
			)
			table_styling = _embed_styling(
				[_CHROMA_NESTED_VERTICAL_ZHUYIN_TABLE], generate_css
			)
			hanzi = syllable["hanzi"]
			result += _HTML_line(f"<td>{hanzi}</td>")
			result += _HTML_line(f"<td {td_styling}>", 1)
			result += _HTML_line(f"<table {table_styling}>", 1)
			result += _HTML_line(f"<tr><td {half_pad_styling}></td></tr>")
			result += _HTML_line("<tr>", 1)
			
		result += _HTML_line(f"<td {class_styling}>", 1)
		result += _HTML_line(f"<span {span_styling}>", 1)
		result += _HTML_line(zhuyin_no_mark)
		result += _HTML_line("</span>", -1)
		result += _HTML_line("</td>", -1)
		result += _HTML_line(f"<td {mark_styling}>{zhuyin_mark}</td>")

		if include_hanzi:
			result += _HTML_line("</tr>", -1)
			result += _HTML_line(f"<tr><td {half_pad_styling}></td></tr>")
			result += _HTML_line("</table>", -1)
			result += _HTML_line("</td>", -1)
		result += _HTML_line(f"<td {half_pad_styling}></td>")

	result += _HTML_line("</tr>", -1)
	result += _HTML_line("</table>", -1)

	return result

# returns a string of HTML formatting with the current tabulation applied.
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

# returns the punctuation HTML added on if merging is specified
# and a boolean indicating if the current cell contents will be empty.
def _return_additional_punctuation(
	syllable_list, category, category_is_tuple, i, j, generate_css
):
	category_name = category[0] if category_is_tuple else category
	syllable = syllable_list[i][j]
	result = ""

	if (
		category_is_tuple
		and category_name in ["pinyin", "ipa", "hanzi_with_zhuyin"]
		and "merge_punctuation" in category
		and syllable["inflection_num"] == 0
	):
		return result, True

	if (
		i + 1 < len(syllable_list)
		and j == len(syllable_list[i]) - 1
		and syllable_list[i + 1][0]["inflection_num"] == 0
	):
		# the next unit is punctuation, 
		# so that is grouped with the current syllable.
		additional_punctuation = syllable_list[i + 1][0]["pinyin"]
		
		# a coloring span is added around the punctuation.
		if not(category_is_tuple and "no_color" in category):
			color_css = _CHROMA_TONES[TO_INFLECTION["none"]]
			styling = _embed_styling([color_css], generate_css)
			result += f"<span {styling}>{additional_punctuation}</span>"
		else:
			result += additional_punctuation
	return result, False

# returns the text that goes after an HTML tag declaration
# to indicate that tag's styling.
def _embed_styling(style_dicts, uses_css):
	if uses_css:
		class_names = " ".join([style_dict["class"] for style_dict in style_dicts])
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