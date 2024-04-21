from ._inflection import TO_INFLECTION
from ._punctuation_marks import PUNCTUATION
from ._vowel_chars import _NEUTRAL_TONE_NUM, get_tone_num, strip_tone_marker
from .color_scheme import _CHROMA_TONES

_HANZI_FONT_SIZE = "32px"
_PINYIN_FONT_SIZE = "13px"
_IPA_FONT_SIZE = "13px"
_ZHUYIN_FONT_SIZE = "13px"
_ZHUYIN_MARK_FONT_SIZE = "13px"

_CHROMA_TABLE = {
	"class": "chroma-table",
	"style": (
		"border-collapse: collapse;",
		"cellpadding = \"0\";",
		"cellspacing = \"0\";",
		"border = \"0\";",
	),
}

_CHROMA_TD = {
	"class": "chroma-td",
	"style": (
		"text-align: center;",
		"vertical-align: center;",
		"padding: 0;",
		"margin: 0;",
	),
}

_CHROMA_HANZI = {
	"class": "chroma-hanzi",
	"style": (
		f"font-size: {_HANZI_FONT_SIZE};",
	),
}

_CHROMA_PINYIN = {
	"class": "chroma-pinyin",
	"style": (
		f"font-size: {_PINYIN_FONT_SIZE};",
	),
}

_CHROMA_IPA = {
	"class": "chroma-ipa",
	"style": (
		f"font-size: {_IPA_FONT_SIZE};",
	),
}

_CHROMA_ZHUYIN = {
	"class": "chroma-zhuyin",
	"style": (
		f"font-size: {_ZHUYIN_FONT_SIZE};",
	),
}

_CHROMA_PITCH_CHART = {
	"class": "chroma-pitch-chart",
	"style": (
		f"font-size: {_ZHUYIN_FONT_SIZE};",
	),
}

_CHROMA_VERTICAL_ZHUYIN_TABLE = {
	"class": "chroma-vertical-zhuyin-table",
	"style": (
		"width: 100%;",
		"height: 100%;",
	),
}

_CHROMA_ZHUYIN_FULL_PAD = {
	"class": "chroma-zhuyin-full-pad",
	"style": (
		"width: 100%;",
		"height: 100%;",
	),
}

_CHROMA_ZHUYIN_HALF_PAD = {
	"class": "chroma-zhuyin-half-pad",
	"style": (
		"width: 50%;",
		"height: 50%;",
	),
}

_CHROMA_VERTICAL_ZHUYIN = {
	"class": "chroma-vertical-zhuyin",
	"style": (
		"writing-mode: vertical-rl;",
		"text-orientation: upright;",
		"white-space: nowrap;",
	),
}

_CHROMA_VERTICAL_ZHUYIN_TEXT = {
	"class": "chroma-vertical-zhuyin-text",
	"style": (
		"width: 0%;",
	),
}

_CHROMA_VERTICAL_ZHUYIN_MARKER = {
	"class": "chroma-vertical-zhuyin-marker",
	"style": (
		f"text-size: {_ZHUYIN_MARK_FONT_SIZE};",
		"vertical-align: bottom;",
		"padding-bottom: 8%;",
		"width: 0%;",
	),
}

_CHROMA_LEFT_ALIGN = {
	"class": "chroma-left-align",
	"style": (
		"text-align: left;",
	),
}

_CHROMA_RIGHT_ALIGN = {
	"class": "chroma-right-align",
	"style": (
		"text-align: right;",
	),
}

_CHROMA_TOP_ALIGN = {
	"class": "chroma-top-align",
	"style": (
		"vertical-align: top;",
	),
}

_CHROMA_BOTTOM_ALIGN = {
	"class": "chroma-bottom-align",
	"style": (
		"vertical-align: bottom;",
	),
}


_CATEGORY_TO_TD_STYLE = {
	"hanzi": _CHROMA_HANZI,
	"hanzi_with_zhuyin": _CHROMA_HANZI,
	"pinyin": _CHROMA_PINYIN,
	"ipa": _CHROMA_IPA,
	"zhuyin": _CHROMA_ZHUYIN,
	"vertical_zhuyin": _CHROMA_ZHUYIN,
	"pitch_chart": _CHROMA_PITCH_CHART,
}

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

# returns the <html_table> and the <css> as a tuple.
def create_stylized_sentence(
	syllable_list,
	categories,
	generate_css,
	vertical=False,
	grouped=True,
	exclude_punctuation=False
):
	html_table = f"<table {_embed_styling([_CHROMA_TABLE], generate_css)}>\n"
	css = ""
	
	if vertical:
		for i, word in enumerate(syllable_list):
			for j, syllable in enumerate(word):
				html_table += "\t<tr>\n"
				for category in categories:
					html_table += _return_td(
						syllable_list,
						category,
						i,
						j,
						generate_css,
						vertical,
						grouped,
						exclude_punctuation
					)
				html_table += "\t</tr>\n"

	else:
		for category in categories:
			html_table += "\t<tr>\n"
			for i, word in enumerate(syllable_list):
				for j, syllable in enumerate(word):
					html_table += _return_td(
						syllable_list,
						category,
						i,
						j,
						generate_css,
						vertical,
						grouped,
						exclude_punctuation
					)
			html_table += "\t</tr>\n"

	html_table += "</table>"

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
	grouped,
	exclude_punctuation
):
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
	result += f"\t\t<td {styling}>"

	# gets the HTML to go inside the <td>.
	result += _return_cell_contents(
		syllable_list,
		category,
		category_is_tuple,
		i,
		j,
		generate_css,
		vertical,
		grouped,
		exclude_punctuation
	)

	# closes all tags and returns the complete <td>...</td> element.
	if category_name in ["vertical_zhuyin"]:
		result += "\n\t\t</td>\n"
	else:
		result += "</td>\n"
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
	grouped,
	exclude_punctuation
):
	syllable = syllable_list[i][j]
	category_name = category[0] if category_is_tuple else category
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
		print(f"{p}\t{inf}")

	if color_css:
		styling = _embed_styling([color_css], generate_css)
		if category_name in ["vertical_zhuyin"]:
			result += "\n\t\t\t"
		result += f"<span {styling}>"


	# 
	if category_name == "hanzi":
		return result + syllable[category_name] + "</span>"

	if category_name == "pinyin":
		if category_is_tuple:
			if "with_nums" in category:
				result += strip_tone_marker(syllable["pinyin"])
				if syllable["tone_num"] != _NEUTRAL_TONE_NUM:
					result += str(syllable["tone_num"])
			elif "no_tones" in category:
				result += strip_tone_marker(syllable["pinyin"])
			else:
				result += syllable["pinyin"]
		else:
			result += syllable["pinyin"]
		
	elif category_name == "ipa":
		if category_is_tuple:
			if "with_nums" in category:
				result += syllable["ipa_root"]
				if syllable["tone_num"] != _NEUTRAL_TONE_NUM:
					result += str(syllable["tone_num"])
			elif "no_tones" in category:
				result += syllable["ipa_root"]
			else:
				result += syllable["ipa"]
		else:
			result = syllable["ipa"]

	elif category_name == "zhuyin":
		if category_is_tuple:
			if "with_nums" in category:
				result += syllable["zhuyin_root"]
				if syllable["tone_num"] != _NEUTRAL_TONE_NUM:
					result += str(syllable["tone_num"])
			elif "no_tones" in category:
				result += syllable["zhuyin_root"]
		else:
			result += syllable["zhuyin"]

	elif category_name == "vertical_zhuyin":
		styling = _embed_styling([_CHROMA_VERTICAL_ZHUYIN_TABLE], generate_css)
		result += f"\n\t\t\t<table style={styling}>\n\t\t\t\t<tr>\n\t\t\t\t\t"
		if grouped and len(syllable_list[j]) > 1:
			if j == 0:
				styling = _embed_styling([_CHROMA_ZHUYIN_FULL_PAD], generate_css)
				result += f"<td {styling}></td>\n\t\t\t\t\t"

			elif not j == len(syllable_list[i]) - 1:
				styling = _embed_styling([_CHROMA_ZHUYIN_HALF_PAD], generate_css)
				result += f"<td {styling}></td>\n\t\t\t\t\t"

			class_styling = _embed_styling(
				[_CHROMA_VERTICAL_ZHUYIN], generate_css
			)
			span_styling = _embed_styling(
				[_CHROMA_VERTICAL_ZHUYIN_TEXT], generate_css
			)
			mark_styling = _embed_styling(
				[_CHROMA_VERTICAL_ZHUYIN_MARKER], generate_css
			)
			zhuyin_no_mark = syllable["zhuyin_prefix"] + syllable["zhuyin_root"]
			zhuyin_mark = syllable["zhuyin_suffix"]
			result += (
				f"<td {class_styling}><span {span_styling}>"
				f"{zhuyin_no_mark}"
				f"</span></td>\n\t\t\t\t\t"
				f"<td {mark_styling}>{zhuyin_mark}</td>\n"
			)

			if j == len(syllable_list[i]) - 1:
				styling = _embed_styling([_CHROMA_ZHUYIN_FULL_PAD], generate_css)
				result += f"<td {styling}></td>\n\t\t\t\t"
			elif not j == 0:
				styling = _embed_styling([_CHROMA_ZHUYIN_HALF_PAD], generate_css)
				result += f"<td {styling}></td>\n\t\t\t\t"
			
		else:
			half_styling = _embed_styling([_CHROMA_ZHUYIN_HALF_PAD], generate_css)
			class_styling = _embed_styling(
				[_CHROMA_VERTICAL_ZHUYIN], generate_css
			)
			span_styling = _embed_styling(
				[_CHROMA_VERTICAL_ZHUYIN_TEXT], generate_css
			)
			mark_styling = _embed_styling(
				[_CHROMA_VERTICAL_ZHUYIN_MARKER], generate_css
			)
			zhuyin_no_mark = syllable["zhuyin_prefix"] + syllable["zhuyin_root"]
			zhuyin_mark = syllable["zhuyin_suffix"]
			result += (
				f"<td {half_styling}></td>\n\t\t\t\t\t"
				f"<td {class_styling}><span {span_styling}>"
				f"{zhuyin_no_mark}"
				f"</span></td>\n\t\t\t\t\t"
				f"<td {mark_styling}>{zhuyin_mark}</td>"
				f"<td {half_styling}></td>\n\t\t\t\t"
			)
		result += "</tr>\n\t\t\t</table>\n\t\t\t"


	# closes color span.
	if color_css:
		result += "</span>"

	# determines the punctuation added on if merging is specified.
	if (
		category_is_tuple
		and category_name in ["pinyin", "ipa"]
		and "merge_punctuation" in category 
	):
		if syllable["inflection_num"] == 0:
			# is punctuation.
			return ""
		
		if (
			i + 1 < len(syllable_list)
			and j == len(syllable_list[i]) - 1
			and syllable_list[i + 1][0]["inflection_num"] == 0
		):
			# the next unit is punctuation, 
			# so that is grouped with the current syllable.
			additional_punctuation = syllable_list[i + 1][0][category_name]
			
			# a coloring span is added around the punctuation.
			if not(category_is_tuple and "no_color" in category):
				color_css = _CHROMA_TONES[TO_INFLECTION["none"]]
				styling = _embed_styling([color_css], generate_css)
				result += f"<span {styling}>{additional_punctuation}</span>"
			else:
				result += additional_punctuation

	return result

# returns the text that goes after an HTML tag declaration
# to indicate that tag's styling.
def _embed_styling(style_dicts, uses_css):
	if uses_css:
		class_names = " ".join([style_dict["class"] for style_dict in style_dicts])
		return f"class=\"{class_names}\""
	return (
		"style=\"" 
		+ " ".join([
			"".join(style_line.split()) 
			for style_dict in style_dicts 
			for style_line in style_dict["style"]]
		) 
		+ "\""
	)