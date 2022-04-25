import wordgen as wg
from random import choice
from os import system
from sys import argv
# get template
template = ""
if len(argv) > 1:
    try:
        with open(argv[1], "r") as f:
            template = f.read()
    except FileNotFoundError:
        exit("no file with name " + argv[1])
else:
    try:
        with open(input("file: "), "r") as f:
            template = f.read()
    except FileNotFoundError:
        exit("no file found")
if template == "": exit()

# reformat template
template = template.replace(" ", "")
template = template.split("\n")
assert len(template) == 3, exit("invalid template")

# get content
GROUPS = template[0]
PATTERNS = [wg.get_pattern(x, GROUPS) for x in template[1].split("/")]
rewrites = {}
if template[2] != "":
    for definition in template[2].split(","):
        split = definition.split(":")
        if len(split) > 1:
            to_rewrite = split[0]
            rewrite = split[1]
            rewrites[to_rewrite] = rewrite
with open(input("word list file: "), "r") as f:
    words_text = f.read()
words = {}
for definition in words_text.split("\n"):
    split = definition.split(":")
    if len(split) > 1:
        word = split[0]
        try: word_patterns = [int(x) for x in split[1].split("/")]
        except ValueError: exit(f"expected a whole number in word pattern options of word '{word}'")
        words[word] = word_patterns

# GENERATE

# control
control = 0
while True:
    try: control = int(input("control? (1/0) "))
    except ValueError: continue
    break
# dictionary generation
dictionary = {}
word_bin = []
gen_word = ""
attempts = 0
for word in words:
    gen_word = wg.generate_word(PATTERNS[choice(words[word])], rewrites)
    while gen_word in word_bin and attempts < 50:
        gen_word = wg.generate_word(PATTERNS[choice(words[word])], rewrites)
        attempts += 1
    attempts = 0
    # control
    while control == 1:
        system("cls")
        print(f"{word}: {gen_word}\n")
        affirmation = input("1/0: ")
        if affirmation == "1": break
        gen_word = wg.generate_word(PATTERNS[choice(words[word])], rewrites)
        while gen_word in word_bin:
            gen_word = wg.generate_word(PATTERNS[choice(words[word])], rewrites)
            attempts += 1
        attempts = 0
    dictionary[word] = gen_word
    word_bin.append(gen_word)

# write to file
with open(input("name: ")+".txt", "w") as f:
    text = ""
    for word in dictionary:
        text +=  f"{word}: {dictionary[word]}\n"
    text = text[:-1]
    f.write(text)