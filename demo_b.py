import chromapinyin


def main():
    chromapinyin.color_scheme.set_punctuation_RGB((255, 255, 255))
    hanzi = "我不是来自中国。"
    pinyin = "wǒ bùshì láizì zhōngguó."
    word_list = chromapinyin.create_word_list(hanzi, pinyin)

    # defines the 2D table of the syllable aspects to display per syllable.
    categories = [
        [
            "hanzi",
            "vertical_zhuyin",
        ],
        [
            (
                "pinyin",
                "number_tones",
            ),
            ("ipa", "no_tones"),
        ],
    ]

    html = ""
    html += "<html>\n<head>\n<style>\n"
    html += "body { background-color: black; }\n</style>\n</head>\n<body>\n"

    # creates an HTML table with styling components placed directly inline
    # and the characters placed to be read horizontally.
    html += chromapinyin.create_stylized_sentence(
        word_list,
        categories,
        use_css=False,
        vertical=False,
        hide_clause_breaks=False,
        max_n_line_syllables=999,
    )
    html += "</body>\n</html>"

    with open("demo_b.html", "w", encoding="utf-8") as file:
        file.write(html)


main()
