# chromapinyin
A python script for creating HTML tables of various Mandarin transcriptions (IPA and zhuyin), with the option to color syllables by their tone.
These can be created by giving the program text in hanzi and its corresponding pinyin.
The program will take the necessary tone changes into account.

## Getting syllable information
```
import chromapinyin

hanzi = "我买雨伞。"
pinyin = "wǒ mǎi yǔsǎn."
syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
```
The ```syllables``` list will contain four lists, with each list representing a "word", a group of syllables.
- ```syllables[0]``` will contain one syllable corresponding to "wǒ" 
- ```syllables[1]``` will contain one syllable corresponding to "mǎi"
- ```syllables[2]``` will contain two syllables corresponding to "yǔ" and "sǎn"
- ```syllables[3]``` will contain one "syllable" corresponding to the "."
<br>
<br>

The contained word list is occupied by dictionary objects which each represent a syllable.
<br>
For example, ```syllables[0][0]``` is a dictionary object with the following keys:
- ```"hanzi": "我"```
- ```"pinyin": "wǒ"```
- ```"tone": "low"```
- ```"tone_num": 3```
- ```"spoken_tone": "rising"```
- ```"spoken_tone_num": 2```
- ```"inflection": "rising_low"```
- ```"inflection_num": 12```
- ```"ipa_root": "u̯ɔ"```
- ```"ipa_suffix": "˧˥"```
- ```"ipa": "u̯ɔ˧˥"```
- ```"zhuyin_prefix": ""```
- ```"zhuyin_root": "ㄨㄛ"```
- ```"zhuyin_suffix": "ˊ"```
- ```"zhuyin": "ㄨㄛˊ"```
