# chromapinyin._stylize._table_css.py
# ---
# this file contains dictionary objects containing CSS information,
# with each dictionary having a <"class"> name and a tuple
# of strings that defines the class's <"style">.
# 
# user functions can be accessed to change font sizes, for example:
# 	chromapinyin.set_pinyin_font_size("30em")
#

import re

__all__ = [
	"CHROMA_DIV_PUSH_LEFT",
	"CHROMA_DIV_PUSH_RIGHT",
	"CHROMA_DIV_PUSH_CENTER",
	"CHROMA_TD_ALIGN_CENTER",
	"CHROMA_TD_ALIGN_TOP",
	"CHROMA_TD_ALIGN_RIGHT",
	"CHROMA_TD_ALIGN_BOTTOM",
	"CHROMA_TD_ALIGN_LEFT",
	"CHROMA_TABLE",
	"CHROMA_TABLE_NESTED",
	"CHROMA_TR",
	"CHROMA_TD",
	"CHROMA_APOSTROPHE_OFFSET",
	"CHROMA_TD_ZHUYIN",
	"CHROMA_DIV_ZHUYIN_CONTAINER",
	"CHROMA_NESTED_ZHUYIN",
	"CHROMA_VERTICAL_ZHUYIN_PREFIX_OFFSET",
	"CHROMA_INLINE_ZHUYIN_PREFIX_OFFSET",
	"CHROMA_ZHUYIN_PREFIX_CONTAINER",
	"CHROMA_ZHUYIN_SUFFIX_OFFSET",
	"CHROMA_VERTICAL_ZHUYIN_SUFFIX_CONTAINER",
	"CHROMA_INLINE_ZHUYIN_SUFFIX_CONTAINER",
	"CHROMA_TD_PITCH_GRAPH",
	"CHROMA_TD_HANDWRITING",
	"get_content_style",
	"category_to_td_style",
	"set_font_sizes",
	"get_content_style_values",
]

# constants are used for setting generic scaling of all components.
_DEFAULT_HANZI_FONT_SIZE = 5
_DEFAULT_HANZI_VERTICAL_OFFSET_PERCENT = -20
_DEFAULT_PINYIN_FONT_SIZE = 1
_DEFAULT_ZHUYIN_PREFIX_FONT_SIZE = 1.6
_DEFAULT_ZHUYIN_ROOT_FONT_SIZE = 1
_DEFAULT_ZHUYIN_SUFFIX_FONT_SIZE = 1.6
_DEFAULT_IPA_FONT_SIZE = 1
_DEFAULT_PITCH_GRAPH_HEIGHT = 5.1
_DEFAULT_HANDWRITING_HEIGHT = 5.12
_DEFAULT_UNIT = "rem"

CHROMA_DIV_PUSH_LEFT = {
	"class": "div.chroma-push-left",
	"style": (
		"margin-right: auto;",
	),
}

CHROMA_DIV_PUSH_RIGHT = {
	"class": "div.chroma-push-right",
	"style": (
		"margin-left: auto;",
	),
}

CHROMA_DIV_PUSH_CENTER = {
	"class": "div.chroma-push-center",
	"style": (
		"margin-left: auto;",
		"margin-right: auto;",
	),
}

CHROMA_TD_ALIGN_CENTER = {
	"class": "td.chroma-align-center",
	"style": (
		"text-align: center;",
		"vertical-align: center;",
	),
}

CHROMA_TD_ALIGN_TOP = {
	"class": "td.chroma-align-top",
	"style": (
		"text-align: center;",
		"vertical-align: top;",
	),
}

CHROMA_TD_ALIGN_RIGHT = {
	"class": "td.chroma-align-right",
	"style": (
		"text-align: right;",
		"vertical-align: center;",
	),
}

CHROMA_TD_ALIGN_BOTTOM = {
	"class": "td.chroma-align-bottom",
	"style": (
		"text-align: center;",
		"vertical-align: bottom;",
	),
}

CHROMA_TD_ALIGN_LEFT = {
	"class": "td.chroma-align-left",
	"style": (
		"text-align: left;",
		"vertical-align: center;",
	),
}

CHROMA_TABLE = {
	"class": "table.chroma",
	"style": (
		"border-collapse: collapse;",
		"border: 0;",
		"margin: 0;",
		"padding: 0;",
		"overflow: visible;",
	),
}

CHROMA_TABLE_NESTED = {
	"class": "table.chroma-nested",
	"style": (
		"border-collapse: collapse;",
		"border: 0;",
		"margin: 0;",
		"padding: 0;",
	),
}

CHROMA_TR = {
	"class": "tr.chroma",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"text-align: center;",
		"overflow: visible;",
	),
}

CHROMA_TD = {
	"class": "td.chroma",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"overflow: visible;",
	),
}

CHROMA_APOSTROPHE_OFFSET = {
	"class": "chroma-apostrophe-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"position: relative;",
		"top: -0.1em;",
	),
}

CHROMA_TD_ZHUYIN = {
	"class": "td.chroma-zhuyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"white-space: nowrap;",
	),
}

CHROMA_DIV_ZHUYIN_CONTAINER = {
	"class": "div.chroma-zhuyin-container",
	"style": (
		"display: table;",
		"text-align: center;",
	),
}

CHROMA_NESTED_ZHUYIN = {
	"class": "chroma-nested-zhuyin",
	"style": (
		"width: 0.2rem;",
		"margin: 0;",
		"padding: 0;",
		"vertical-align: bottom;",
	),
}

CHROMA_VERTICAL_ZHUYIN_PREFIX_OFFSET = {
	"class": "chroma-vertical-zhuyin-prefix-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"display: flex;",
		"position: relative;",
		"left: 0.3em;",
		"top: -0.5em;",
	),
}

CHROMA_INLINE_ZHUYIN_PREFIX_OFFSET = {
	"class": "chroma-inline-zhuyin-prefix-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"display: flex;",
		"position: relative;",
		"left: 0em;",
		"top: 0.1em;",
	),
}

CHROMA_ZHUYIN_PREFIX_CONTAINER = {
	"class": "chroma-zhuyin-prefix-container",
	"style": (
		"width: 0.2em;",
		"height: 0.06em;",
		"display: flex;",
		"position: relative;",
	)
}

CHROMA_ZHUYIN_SUFFIX_OFFSET = {
	"class": "chroma-zhuyin-suffix-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"display:flex;",
		"position: relative;",
		"left: -0.2em;",
		"top: -1.42em;",
	),
}

CHROMA_VERTICAL_ZHUYIN_SUFFIX_CONTAINER = {
	"class": "chroma-vertical-zhuyin-suffix-container",
	"style": (
		"width: 0.32em;",
		"height: 0;",
		"display: flex;",
		"position: relative;",
	)
}

CHROMA_INLINE_ZHUYIN_SUFFIX_CONTAINER = {
	"class": "chroma-inline-zhuyin-suffix-container",
	"style": (
		"width: 0rem;",
		"height: 0;",
		"display: flex;",
		"position: relative;",
	)
}

CHROMA_TD_PITCH_GRAPH = {
	"class": "td.chroma-pitch-graph",
	"style": (
		"margin: 0;",
		"padding: 0;"
	),
}

CHROMA_TD_HANDWRITING = {
	"class": "td.chroma-handwriting",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"position: relative;",
		"overflow: visible;",
	),
}

_CONTENT_STYLES = {}
_TO_TD_STYLE = {
	"hanzi": None,
	"pinyin": None,
	"zhuyin": CHROMA_TD_ZHUYIN,
	"vertical_zhuyin": CHROMA_TD_ZHUYIN,
	"ipa": None,
	"pitch_graph": CHROMA_TD_PITCH_GRAPH,
	"handwriting": CHROMA_TD_HANDWRITING,
}

# sets every font size of each component to a default size times <scale>.
def set_font_sizes(scale=1.0):
	set_hanzi_font_size(f"{(_DEFAULT_HANZI_FONT_SIZE * scale):.3f}{_DEFAULT_UNIT}")
	set_hanzi_vertical_offset()
	set_pinyin_font_size(f"{(_DEFAULT_PINYIN_FONT_SIZE * scale):.3f}{_DEFAULT_UNIT}")
	set_zhuyin_prefix_font_size(
		f"{(_DEFAULT_ZHUYIN_PREFIX_FONT_SIZE * scale):.3f}{_DEFAULT_UNIT}"
	)
	set_zhuyin_root_font_size(
		f"{(_DEFAULT_ZHUYIN_ROOT_FONT_SIZE * scale):.3f}{_DEFAULT_UNIT}"
	)
	set_zhuyin_suffix_font_size(
		f"{(_DEFAULT_ZHUYIN_SUFFIX_FONT_SIZE * scale):.3f}{_DEFAULT_UNIT}"
	)
	set_ipa_font_size(f"{(_DEFAULT_IPA_FONT_SIZE * scale):.3f}{_DEFAULT_UNIT}")
	set_pitch_graph_height(f"{(_DEFAULT_PITCH_GRAPH_HEIGHT * scale):.3f}{_DEFAULT_UNIT}")
	set_handwriting_height(f"{(_DEFAULT_HANDWRITING_HEIGHT * scale):.3f}{_DEFAULT_UNIT}")

# returns the corresponding dictionary containing CSS information.
def get_content_style(key_name):
	global _CONTENT_STYLES
	return _CONTENT_STYLES[key_name]

# returns the corresponding dictionary containing CSS information.
def category_to_td_style(category):
	global _TO_TD_STYLE
	return _TO_TD_STYLE[category]

def set_hanzi_font_size(font_size=f"{_DEFAULT_HANZI_FONT_SIZE:.3f}{_DEFAULT_UNIT}"):
	global _CONTENT_STYLES, _TO_TD_STYLE
	_CONTENT_STYLES["CHROMA_TD_HANZI"] = {
		"class": "td.chroma-hanzi",
		"style": (
			"margin: 0;",
			"padding-top: 0.1rem;",
			"padding-right: 0.0rem;",
			"padding-bottom: 0.1rem;",
			"padding-left: 0.07rem;",
			f"font-size: {font_size};",
			"font-family: SimHei;"
		),
	}

	_CONTENT_STYLES["CHROMA_DIV_HANZI_CONTAINER"] = {
		"class": "div.chroma-hanzi-container",
		"style": (
			f"height: {font_size};",
			"display: block;",
			"overflow: hidden;",
			"position: relative;",
		),
	}
	_TO_TD_STYLE["hanzi"] = _CONTENT_STYLES["CHROMA_TD_HANZI"]

def set_hanzi_vertical_offset(
	vertical_offset=f"{_DEFAULT_HANZI_VERTICAL_OFFSET_PERCENT:.3f}%"
):
	global _CONTENT_STYLES
	_CONTENT_STYLES["CHROMA_HANZI_OFFSET"] = {
		"class": "chroma-hanzi-offset",
		"style": (
			"display: block;",
			"position: relative;",
			f"top: {vertical_offset};",
		),
	}

def set_pinyin_font_size(font_size=f"{_DEFAULT_PINYIN_FONT_SIZE:.3f}{_DEFAULT_UNIT}"):
	global _CONTENT_STYLES, _TO_TD_STYLE
	_CONTENT_STYLES["CHROMA_TD_PINYIN"] = {
		"class": "td.chroma-pinyin",
		"style": (
			"margin: 0;",
			"padding: 0;",
			f"font-size: {font_size};"
		),
	}
	_TO_TD_STYLE["pinyin"] = _CONTENT_STYLES["CHROMA_TD_PINYIN"]

def set_zhuyin_font_size(font_size=f"{_DEFAULT_ZHUYIN_ROOT_FONT_SIZE:.3f}{_DEFAULT_UNIT}"):
	set_zhuyin_prefix_font_size(font_size)
	set_zhuyin_root_font_size(font_size)
	set_zhuyin_suffix_font_size(font_size)

def set_zhuyin_prefix_font_size(
	font_size=f"{_DEFAULT_ZHUYIN_PREFIX_FONT_SIZE:.3f}{_DEFAULT_UNIT}"
):
	global _CONTENT_STYLES
	_CONTENT_STYLES["CHROMA_ZHUYIN_PREFIX"] = {
		"class": "chroma-zhuyin-prefix",
		"style": (
			f"font-size: {font_size};",
		),
	}

def set_zhuyin_root_font_size(font_size=f"{_DEFAULT_ZHUYIN_ROOT_FONT_SIZE:.3f}{_DEFAULT_UNIT}"):
	global _CONTENT_STYLES
	_CONTENT_STYLES["CHROMA_ZHUYIN_ROOT"] = {
		"class": "chroma-zhuyin-root",
		"style": (
			f"font-size: {font_size};",
		),
	}

	_CONTENT_STYLES["CHROMA_INLINE_ZHUYIN"] = {
		"class": "chroma-inline-zhuyin",
		"style": (
			f"height: {font_size};",
			"margin: 0;",
			"padding: 0;",
			"display: flex;",
			"position: relative;",
			"white-space: nowrap;",
			"overflow: visible;",
		),
	}

	_CONTENT_STYLES["CHROMA_VERTICAL_ZHUYIN"] = {
		"class": "chroma-vertical-zhuyin",
		"style": (
			"margin: 0;",
			"padding: 0;",
			"display: flex;",
			"position: relative;",
			"text-orientation: upright;",
			"writing-mode: vertical-lr;",
			"white-space: nowrap;",
			"overflow: hidden;",
		),
	}

	_CONTENT_STYLES["CHROMA_TD_NESTED_VERTICAL_ZHUYIN_ROOT"] = {
		"class": "td.chroma-nested-vertical-zhuyin-root",
		"style": (
			f"width: {font_size};",
			"margin: 0;",
			"padding: 0;",
			"vertical-align: bottom;",
		),
	}
	

def set_zhuyin_suffix_font_size(
	font_size=f"{_DEFAULT_ZHUYIN_SUFFIX_FONT_SIZE:.3f}{_DEFAULT_UNIT}"
):
	global _CONTENT_STYLES
	_CONTENT_STYLES["CHROMA_ZHUYIN_SUFFIX"] = {
		"class": "chroma-zhuyin-suffix",
		"style": (
			f"font-size: {font_size};",
		),
	}

def set_ipa_font_size(font_size=f"{_DEFAULT_IPA_FONT_SIZE:.3f}{_DEFAULT_UNIT}"):
	global _CONTENT_STYLES, _TO_TD_STYLE
	_CONTENT_STYLES["CHROMA_TD_IPA"] = {
		"class": "td.chroma-ipa",
		"style": (
			"margin: 0;",
			"padding: 0;",
			f"font-size: {font_size};",
		),
	}
	_TO_TD_STYLE["ipa"] = _CONTENT_STYLES["CHROMA_TD_IPA"]

def set_pitch_graph_height(height=f"{_DEFAULT_PITCH_GRAPH_HEIGHT:.3f}{_DEFAULT_UNIT}"):
	global _CONTENT_STYLES
	_CONTENT_STYLES["CHROMA_IMG_PITCH_GRAPH"] = {
		"class": "img.chroma-pitch-graph",
		"style": (
			f"height: {height};",
			"object-fit: contain;",
		),
	}

def set_handwriting_height(height=f"{_DEFAULT_HANDWRITING_HEIGHT:.3f}{_DEFAULT_UNIT}"):
	global _CONTENT_STYLES
	_CONTENT_STYLES["CHROMA_IMG_HANDWRITING"] = {
		"class": "img.chroma-handwriting",
		"style": (
			f"height: {height};",
			"object-fit: contain;",
		),
	}

def get_content_style_values():
	return _CONTENT_STYLES.values()

set_font_sizes(1.0) # initializes <_CONTENT_STYLES> elements.