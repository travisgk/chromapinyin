from chromapinyin.vowel_chars import (
	get_tone_num, strip_tone_marker, place_tone_marker
)
from chromapinyin.syllable import create_syllable_dict
import chromapinyin.sequential_inflection
import chromapinyin.to_syllable_list

def main():
	sample_list = "shén me shí hòu".split()
	for syllable in sample_list:
		tone_num = get_tone_num(syllable)
		stripped = strip_tone_marker(syllable)
		print(place_tone_marker(stripped, tone_num))

	syllable = create_syllable_dict("我", "wǒ", 3)
	print(syllable)

	pinyin = "lǎobǎn xiǎng mǎi nǎ zhǒng shuǐguǒ."
	inflections = [[3, 3], [3], [3], [3], [3], [3, 3]]
	chromapinyin.sequential_inflection.apply_rule(inflections, 3, 2)
	print(chromapinyin.to_syllable_list.split_pinyin(pinyin))
	print("\n")

	pinyin = "lǐ lǎobǎn xiǎng zhǎo nǐ yǎnjiǎng."
	inflections = [[3], [3, 3], [3], [3], [3], [3, 3]]
	chromapinyin.sequential_inflection.apply_rule(inflections, 3, 2)
	print(chromapinyin.to_syllable_list.split_pinyin(pinyin))
	print("\n")

	pinyin = "wǒ bǐ nǐ xiǎo."
	inflections = [[3], [3], [3], [3]]
	chromapinyin.sequential_inflection.apply_rule(inflections, 3, 2)
	print(chromapinyin.to_syllable_list.split_pinyin(pinyin))
	print("\n")

	pinyin = "wǒ mǎi yǔsǎn."
	inflections = [[3], [3], [3, 3]]
	chromapinyin.sequential_inflection.apply_rule(inflections, 3, 2)
	print(chromapinyin.to_syllable_list.split_pinyin(pinyin))
	print("\n")

	pinyin = "wǒ yě xiǎng mǎi ba xiǎo yǔsǎn."
	inflections = [[3], [3], [3], [3], [0], [3], [3, 3]]
	chromapinyin.sequential_inflection.apply_rule(inflections, 3, 2)
	print(chromapinyin.to_syllable_list.split_pinyin(pinyin))
	print("\n")

	pinyin = "wǒ hěn hǎo."
	inflections = [[3], [3], [3]]
	chromapinyin.sequential_inflection.apply_rule(inflections, 3, 2)
	print(chromapinyin.to_syllable_list.split_pinyin(pinyin))
	print("\n")

	pinyin = "hěn yǒnggǎn."
	inflections = [[3], [3, 3]]
	chromapinyin.sequential_inflection.apply_rule(inflections, 3, 2)
	print(chromapinyin.to_syllable_list.split_pinyin(pinyin))
	print("\n")

	

main()