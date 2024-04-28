import chromapinyin
from chromapinyin._stylize._pitch_graphs._pitch_graphs import save_inflection_graphs

def main():
	save_inflection_graphs()
	css = chromapinyin.generate_CSS()
	print(css)

	phrases = [
		
		{"hanzi": "我不是来自中国。"		, "pinyin": "wǒ bùshì láizì zhōngguó."},
		{"hanzi": "晚安。"				, "pinyin": "wǎn'ān."},
		{"hanzi": "我也很好。"			, "pinyin": "wǒ yě hěn hǎo." },
		{"hanzi": "你叫什么名字？"		, "pinyin": "nǐ jiào shénme míngzi?"},
	]
	
	# prints out an HTML table for every phrase in <phrases>.
	for i, phrase in enumerate(phrases):
		word_list = chromapinyin.create_word_list(
			phrase["hanzi"], phrase["pinyin"]
		)

		categories = ["hanzi"]
		if i == 2:
			categories = [
				[("hanzi", "grouped"), ("vertical_zhuyin",)], 
				[("pinyin", "merge_punctuation", "grouped",),],
			]
		elif i == 3:
			categories = [
				[("hanzi", "grouped"), ("ipa", "no_tones"),], 
				[("pinyin", "merge_punctuation", "grouped",),],
			]
		else:
			categories = [
				[("hanzi", "grouped"),], 
				[("pinyin", "merge_punctuation", "grouped",),],
				[("vertical_zhuyin",)],
			]

		html = chromapinyin.create_stylized_sentence(
			word_list, 
			categories,
			use_css=True,
			vertical = i == 2,
			max_n_line_syllables = 3 if i == 3 else 99
		)
		print(html)
		if i < len(phrases) - 1:
			print("\n<br>\n<br>")

main()