import os
import chromapinyin


def main():
    chromapinyin.set_pitch_graph_height("7em")
    chromapinyin.color_scheme.set_punctuation_RGB((255, 255, 255))
    chromapinyin.create_inflection_graphs(fixed_width=True, style_name="fancy")
    css = chromapinyin.generate_CSS()

    hanzi = "很高兴认识你"
    pinyin = "hěn gāoxìng rènshí nǐ"
    word_list = chromapinyin.create_word_list(hanzi, pinyin)

    # a 2D table of the syllable aspects to display.
    categories = [
        ["hanzi", "vertical_zhuyin"],
        [("pinyin", "grouped")],
        [("pitch_graph", "grouped")],
    ]

    html = ""
    html += "<html>\n<head>\n<style>\nbody {\n"
    html += "\tfont-family: DejaVu Sans;\n\tbackground-color: black;\n}\n\n"
    html += css
    html += '</style>\n</head>\n<body>\n<div class="nightMode">\n'

    # creates an HTML table with styling components placed directly inline
    # and the characters placed to be read horizontally.
    html += chromapinyin.create_stylized_sentence(
        word_list,
        categories,
        use_css=True,
        vertical=False,
        hide_clause_breaks=False,
        max_n_line_syllables=999,
    )
    html += "</div>\n</body>\n</html>"

    output_path = os.path.join(chromapinyin.get_output_dir(), "demo_a.html")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)


if __name__ == "__main__":
    main()
