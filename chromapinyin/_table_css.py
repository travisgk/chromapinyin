__all__ = [
	"_CHROMA_TABLE",
	"_CHROMA_TD",
	"_CHROMA_HANZI",
	"_CHROMA_PINYIN",
	"_CHROMA_IPA",
	"_CHROMA_ZHUYIN",
	"_CHROMA_PITCH_CHART",
	"_CHROMA_VERTICAL_ZHUYIN_TABLE",
	"_CHROMA_ZHUYIN_BY_HANZI_TD",
	"_CHROMA_NESTED_VERTICAL_ZHUYIN_TABLE",
	"_CHROMA_FULL_PAD",
	"_CHROMA_HALF_PAD",
	"_CHROMA_VERTICAL_TEXT",
	"_CHROMA_VERTICAL_ZHUYIN_ROOT",
	"_CHROMA_VERTICAL_SINGLE_ZHUYIN_MARKER",
	"_CHROMA_VERTICAL_MULTI_ZHUYIN_MARKER",
	"_CHROMA_LEFT_ALIGN",
	"_CHROMA_RIGHT_ALIGN",
	"_CHROMA_TOP_ALIGN",
	"_CHROMA_BOTTOM_ALIGN",
	"_CATEGORY_TO_TD_STYLE",
]

_HANZI_FONT_SIZE = "64px"
_PINYIN_FONT_SIZE = "13px"
_IPA_FONT_SIZE = "13px"
_ZHUYIN_FONT_SIZE = "13px"
_SUB_ZHUYIN_ROOT_FONT_SIZE = "13px"
_SUB_ZHUYIN_MARK_FONT_SIZE = "13px"

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
		"",
	),
}

_CHROMA_VERTICAL_ZHUYIN_TABLE = {
	"class": "chroma-vertical-zhuyin-table",
	"style": (
		"width: 100%;",
		"height: 100%;",
		"border-collapse: collapse;",
		"cellpadding = \"0\";",
		"cellspacing = \"0\";",
		"border = \"0\";",
		"background-color: #0000ff;",
	),
}

_CHROMA_ZHUYIN_BY_HANZI_TD = {
	"class": "chroma-zhuyin-by-hanzi-td",
	"style": (
		"vertical-align: bottom;",
		"padding-top: 10%;",
		"padding-right: 0;",
		"padding-bottom: 0;",
		"padding-left: 0;",
		"background-color: #009900;",
	),
}

_CHROMA_NESTED_VERTICAL_ZHUYIN_TABLE = {
	"class": "chroma-nested-vertical-zhuyin-table",
	"style": (
		"height: 100%;",
		"border-collapse: collapse;",
		"cellpadding = \"0\";",
		"cellspacing = \"0\";",
		"border = \"0\";",
		"background-color: #005555;",
	),
}

_CHROMA_FULL_PAD = {
	"class": "chroma-zhuyin-full-pad",
	"style": (
		"width: 100%;",
		"height: 100%;",
		"margin: 0;",
		"padding: 0;",
	),
}

_CHROMA_HALF_PAD = {
	"class": "chroma-zhuyin-half-pad",
	"style": (
		"width: 50%;",
		"height: 50%;",
		"margin: 0;",
		"padding: 0;",
	),
}

_CHROMA_VERTICAL_TEXT = {
	"class": "chroma-vertical-text",
	"style": (
		"writing-mode: vertical-lr;",
		"text-orientation: upright;",
		"white-space: nowrap;",
	),
}

_CHROMA_VERTICAL_ZHUYIN_ROOT = {
	"class": "chroma-vertical-zhuyin-root",
	"style": (
		f"font-size: {_SUB_ZHUYIN_ROOT_FONT_SIZE};",
		"vertical-align: center;",
		"width: 0%;",
		"margin: 0;",
		"padding: 0;",
		"background-color: #33bb99;",
	),
}

_CHROMA_VERTICAL_SINGLE_ZHUYIN_MARKER = {
	"class": "chroma-vertical-single-zhuyin-marker",
	"style": (
		f"font-size: {_SUB_ZHUYIN_MARK_FONT_SIZE};",
		"vertical-align: top;",
		"padding-top: 12%;",
		"width: 0%;",
		"margin: 0;",
		"padding: 0;",
		"background-color: #990099;",
	),
}

_CHROMA_VERTICAL_MULTI_ZHUYIN_MARKER = {
	"class": "chroma-vertical-multi-zhuyin-marker",
	"style": (
		f"font-size: {_SUB_ZHUYIN_MARK_FONT_SIZE};",
		"vertical-align: bottom;",
		"padding-bottom: 8px;",
		"width: 0%;",
		"background-color: #330099;",
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