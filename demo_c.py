import os
import chromapinyin


def main():
    chromapinyin.color_scheme.set_punctuation_RGB((255, 255, 255))
    hanzi = "你叫什么名字"
    pinyin = "nǐ jiào shénme míngzi?"
    word_list = chromapinyin.create_word_list(hanzi, pinyin)

    # defines the 2D table of the syllable aspects to display per syllable.
    categories = [
        ["hanzi", "vertical_zhuyin", "pinyin"],
        ["zhuyin", "blank", ("ipa", "no_color", "no_tones")],
        [("handwriting", "night_mode_GIFs")],
    ]

    html = ""
    html += "<html>\n<head>\n<style>\n"
    html += (
        "body { background-color: black; color: white; }\n</style>\n</head>\n<body>\n"
    )

    # creates an HTML table with styling components placed directly inline
    # and the characters placed to be read horizontally.
    html += chromapinyin.create_stylized_sentence(
        word_list,
        categories,
        use_css=False,
        vertical=False,
        hide_clause_breaks=False,
        max_n_line_syllables=5,
    )
    html += "</body>\n</html>"

    output_path = os.path.join(chromapinyin.get_output_dir(), "demo_c.html")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)


if __name__ == "__main__":
    main()
