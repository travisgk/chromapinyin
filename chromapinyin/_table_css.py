__all__ = [
	"_CHROMA_DIV_PUSH_LEFT",
	"_CHROMA_DIV_PUSH_RIGHT",
	"_CHROMA_DIV_PUSH_CENTER",
	"_CHROMA_TD_ALIGN_CENTER",
	"_CHROMA_TD_ALIGN_TOP",
	"_CHROMA_TD_ALIGN_RIGHT",
	"_CHROMA_TD_ALIGN_BOTTOM",
	"_CHROMA_TD_ALIGN_LEFT",
	"_CHROMA_TABLE",
	"_CHROMA_TR",
	"_CHROMA_TD",
	"_CHROMA_TD_HANZI",
	"_CHROMA_DIV_HANZI_CONTAINER",
	"_CHROMA_HANZI_OFFSET",
	"_CHROMA_TD_PINYIN",
	"_CHROMA_TD_ZHUYIN",
	"_CHROMA_DIV_ZHUYIN_CONTAINER",
	"_CHROMA_NESTED_ZHUYIN",
	"_CHROMA_ZHUYIN_PREFIX",
	"_CHROMA_ZHUYIN_ROOT",
	"_CHROMA_ZHUYIN_SUFFIX",
	"_CHROMA_ZHUYIN_PREFIX_OFFSET",
	"_CHROMA_ZHUYIN_SUFFIX_OFFSET",
	"_CHROMA_VERTICAL_ZHUYIN",
	"_CHROMA_APOSTROPHE_OFFSET",
	"_CHROMA_TD_IPA",
	"_CHROMA_TD_PITCH_CHART",
	"_CATEGORY_TO_TD_STYLE",
]

_HANZI_FONT_SIZE = "64px"
_HANZI_VERTICAL_OFFSET = "-20%";
_PINYIN_FONT_SIZE = "13px"
_ZHUYIN_PREFIX_FONT_SIZE = "21px"
_ZHUYIN_ROOT_FONT_SIZE = "13px"
_ZHUYIN_SUFFIX_FONT_SIZE = "21px"
_IPA_FONT_SIZE = "13px"

_CHROMA_DIV_PUSH_LEFT = {
	"class": "div.chroma-push-left",
	"style": (
		"margin-right: auto;",
	),
}

_CHROMA_DIV_PUSH_RIGHT = {
	"class": "div.chroma-push-right",
	"style": (
		"margin-left: auto;",
	),
}

_CHROMA_DIV_PUSH_CENTER = {
	"class": "div.chroma-push-center",
	"style": (
		"margin-left: auto;",
		"margin-right: auto;",
	),
}

_CHROMA_TD_ALIGN_CENTER = {
	"class": "td.chroma-align-center",
	"style": (
		"text-align: center;",
		"vertical-align: center;",
	),
}

_CHROMA_TD_ALIGN_TOP = {
	"class": "td.chroma-align-top",
	"style": (
		"text-align: center;",
		"vertical-align: top;",
	),
}

_CHROMA_TD_ALIGN_RIGHT = {
	"class": "td.chroma-align-right",
	"style": (
		"text-align: right;",
		"vertical-align: center;",
	),
}

_CHROMA_TD_ALIGN_BOTTOM = {
	"class": "td.chroma-align-bottom",
	"style": (
		"text-align: center;",
		"vertical-align: bottom;",
	),
}

_CHROMA_TD_ALIGN_LEFT = {
	"class": "td.chroma-align-left",
	"style": (
		"text-align: left;",
		"vertical-align: center;",
	),
}

_CHROMA_TABLE = {
	"class": "table.chroma",
	"style": (
		"border-collapse: collapse;",
		"border: 0;",
		"margin: 0;",
		"padding: 0;",
	),
}

_CHROMA_TR = {
	"class": "tr.chroma",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

_CHROMA_TD = {
	"class": "td.chroma",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

_CHROMA_TD_HANZI = {
	"class": "td.chroma-hanzi",
	"style": (
		"margin: 0;",
		"padding: 1px;",
		f"font-size: {_HANZI_FONT_SIZE};",
	),
}

_CHROMA_DIV_HANZI_CONTAINER = {
	"class": "div.chroma-hanzi-container",
	"style": (
		"display: block;",
		"overflow: hidden;",
		"position: relative;",
		f"height: {_HANZI_FONT_SIZE};",
	),
}

_CHROMA_HANZI_OFFSET = {
	"class": "chroma-hanzi-offset",
	"style": (
		"display: block;",
		"position: relative;",
		f"top: {_HANZI_VERTICAL_OFFSET};",
	),
}

_CHROMA_TD_PINYIN = {
	"class": "td.chroma-pinyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
		f"font-size: {_PINYIN_FONT_SIZE};"
	),
}

_CHROMA_TD_ZHUYIN = {
	"class": "td.chroma-zhuyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

_CHROMA_DIV_ZHUYIN_CONTAINER = {
	"class": "div.chroma-zhuyin-container",
	"style": (
		"display: table;",
		"overflow: hidden;",
	),
}

_CHROMA_NESTED_ZHUYIN = {
	"class": "chroma-nested-zhuyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"width: 5px;",
		"vertical-align: bottom;",
	),
}

_CHROMA_ZHUYIN_PREFIX = {
	"class": "chroma-zhuyin-prefix",
	"style": (
		f"font-size: {_ZHUYIN_PREFIX_FONT_SIZE};",
	),
}

_CHROMA_ZHUYIN_ROOT = {
	"class": "chroma-zhuyin-root",
	"style": (
		f"font-size: {_ZHUYIN_ROOT_FONT_SIZE};",
	),
}

_CHROMA_ZHUYIN_SUFFIX = {
	"class": "chroma-zhuyin-suffix",
	"style": (
		f"font-size: {_ZHUYIN_SUFFIX_FONT_SIZE};",
	),
}

_CHROMA_ZHUYIN_PREFIX_OFFSET = {
	"class": "chroma-zhuyin-prefix-offset",
	"style": (
		"position: relative;",
		"display: block;",
		"height: 5px;",
		"top: -4px;",
		"z-index: 3;"
	),
}

_CHROMA_ZHUYIN_SUFFIX_OFFSET = {
	"class": "chroma-zhuyin-suffix-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"position: relative;",
		"top: -2px;",
	),
}

_CHROMA_VERTICAL_ZHUYIN = {
	"class": "chroma-vertical-zhuyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"display: flex;",
		"position: relative;",
		"text-orientation: upright;",
		"writing-mode: vertical-lr;",
		"white-space: nowrap;",
	),
}

_CHROMA_APOSTROPHE_OFFSET = {
	"class": "chroma-apostrophe-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"position: relative;",
		"top: -2px;",
	),
}

_CHROMA_TD_IPA = {
	"class": "td.chroma-ipa",
	"style": (
		"margin: 0;",
		"padding: 0;",
		f"font-size: {_IPA_FONT_SIZE};",
	),
}

_CHROMA_TD_PITCH_CHART = {
	"class": "td.chroma-pitch-chart",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

_CATEGORY_TO_TD_STYLE = {
	"hanzi": _CHROMA_TD_HANZI,
	"pinyin": _CHROMA_TD_PINYIN,
	"zhuyin": _CHROMA_TD_ZHUYIN,
	"vertical_zhuyin": _CHROMA_TD_ZHUYIN,
	"ipa": _CHROMA_TD_IPA,
	"pitch_chart": _CHROMA_TD_PITCH_CHART,
}