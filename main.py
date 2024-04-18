from chromapinyin.vowel_chars import (
	get_tone_num, strip_tone_marker, place_tone_marker
)
import chromapinyin.syllables

def main():
	sample_list = "shén me shí hòu".split()
	for syllable in sample_list:
		tone_num = get_tone_num(syllable)
		stripped = strip_tone_marker(syllable)
		print(place_tone_marker(stripped, tone_num), end=" ")
	print("\n")

	hanzi = "老板想买哪种水果。"
	pinyin = "lǎobǎn xiǎng mǎi nǎ zhǒng shuǐguǒ."
	inflections = [[3, 3], [3], [3], [3], [3], [3, 3]]
	syllables = chromapinyin.syllables.create_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "李老板想找你演讲。"
	pinyin = "lǐ lǎobǎn xiǎng zhǎo nǐ yǎnjiǎng."
	inflections = [[3], [3, 3], [3], [3], [3], [3, 3]]
	syllables = chromapinyin.syllables.create_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "我比你小。"
	pinyin = "wǒ bǐ nǐ xiǎo."
	inflections = [[3], [3], [3], [3]]
	syllables = chromapinyin.syllables.create_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "我买与散。"
	pinyin = "wǒ mǎi yǔsǎn."
	inflections = [[3], [3], [3, 3]]
	syllables = chromapinyin.syllables.create_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "我很好。"
	pinyin = "wǒ hěn hǎo."
	inflections = [[3], [3], [3]]
	syllables = chromapinyin.syllables.create_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "很勇敢。"
	pinyin = "hěn yǒnggǎn."
	inflections = [[3], [3, 3]]
	syllables = chromapinyin.syllables.create_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

main()