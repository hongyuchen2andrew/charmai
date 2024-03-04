

def print_fixed_word_count(text, words_per_line):
    words = text.split()
    lines = []
    line = []

    for word in words:
        line.append(word)
        if len(line) >= words_per_line:
            lines.append(" ".join(line))
            line = []

    if line:
        lines.append(" ".join(line))

    for line in lines:
        print(line)
