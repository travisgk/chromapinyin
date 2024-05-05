import chromapinyin


def main():
    chromapinyin.color_scheme.set_punctuation_RGB((255, 255, 255))
    chromapinyin.create_inflection_graphs(fixed_width=True, style_name="simple")
    chromapinyin.set_ipa_font_size("0.5em")

    hanzi = "它很美。"
    pinyin = "tā hěn měi."
    word_list = chromapinyin.create_word_list(hanzi, pinyin)

    # defines the 2D table of the syllable aspects to display per syllable.
    categories = [
        [
            "hanzi",
        ],
        [
            "pinyin",
            (
                "ipa",
                "no_tones",
            ),
        ],
        [
            "zhuyin",
        ],
        [
            ("pitch_graph", "grouped"),
        ],
    ]

    html = ""
    html += "<html>\n<head>\n<style>\n"
    html += (
        'body { background-color: black; color: white; font-family: "DejaVu Sans"; }'
    )
    html += "</style>\n</head>\n<body>\n"

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

    with open("demo_e.html", "w", encoding="utf-8") as file:
        file.write(html)


main()
