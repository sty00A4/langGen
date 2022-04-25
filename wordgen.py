from string import ascii_letters as LETTERS
from random import choice, randint
class Letter:
    def __init__(self, letter: str):
        self.letter = letter
    def __repr__(self):
        return self.letter
    def gen(self):
        return self.letter
    def __str__(self):
        return repr(self)
class Group:
    def __init__(self, letters: list):
        self.letters = letters
    def gen(self):
        return choice(self.letters).gen()
    def __repr__(self):
        return "{" + f"{','.join(str(x) for x in self.letters)}" + "}"
    def __str__(self):
        return repr(self)
class Pattern:
    def __init__(self, pattern: list):
        self.pattern = pattern
    def __repr__(self):
        return f"{repr(self.pattern)}"
    def gen(self):
        word = ""
        for e in self.pattern:
            word += e.gen()
        return word
    def __str__(self):
        return repr(self)
class Optional:
    def __init__(self, content: Pattern):
        self.content = content
    def gen(self):
        return self.content.gen() if randint(0, 1) == 1 else ""
    def __repr__(self):
        return f"({repr(self.content)})"
    def __str__(self):
        return repr(self)
def gen_groups(raw):
    groups = {}
    for i, group in enumerate(raw.split(",")):
        temp = group.split(":")
        assert len(temp) > 1, exit(f"expected ':', group {i}")
        assert len(temp) == 2, exit(f"invalid syntax, group {i}")
        assert len(temp[0]) == 1, exit(f"group labels have to be just one letter, group {i}")
        assert temp[0].isupper(), exit(f"group labels have to be upper case, group {i}")
        assert len(temp[1]) > 0, exit(f"no letters in group, group {i}")
        groups[temp[0]] = Group([Letter(x) for x in temp[1]])
    return groups
def tokenize(raw: str, groups: dict):
    i = 0
    pattern = []
    while i < len(raw):
        if raw[i] in LETTERS:
            if raw[i].isupper():
                assert raw[i] in groups, exit(f"group not defined, idx {i} of pattern")
                pattern.append(groups[raw[i]])
            else:
                pattern.append(Letter(raw[i]))
        elif raw[i] == "(":
            count = 1
            temp = ""
            while i < len(raw) and count > 0:
                i += 1
                temp += raw[i]
                if raw[i] == "(": count += 1
                if raw[i] == ")": count -= 1
            temp = temp[:-1]
            pattern.append(Optional(Pattern(tokenize(temp, groups))))
        elif raw[i] == "[":
            count = 1
            temp = ""
            temp2 = []
            while i < len(raw) and count > 0:
                i += 1
                if i < len(raw):
                    if raw[i] == "," and count == 1:
                        temp2.append(temp)
                        temp = ""
                        continue
                    temp += raw[i]
                    if raw[i] == "[": count += 1
                    if raw[i] == "]": count -= 1
            temp = temp[:-1]
            temp2.append(temp)
            pattern.append(Group([Pattern(tokenize(x, groups)) for x in temp2]))
        i += 1
    return pattern
def get_pattern(pattern, groups):
    return Pattern(tokenize(pattern, gen_groups(groups)))
def generate_word(pattern: Pattern, rewrites: dict):
    word = pattern.gen()
    for rewrite in rewrites:
        if rewrite in word:
            word = word.replace(rewrite, rewrites[rewrite])
    return word