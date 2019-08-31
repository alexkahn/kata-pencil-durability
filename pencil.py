import re
from string import ascii_lowercase, ascii_uppercase

from eraser import Eraser


def make_re(n_spaces):
    return re.compile(r"(\s{1})\s{" + re.escape(str(n_spaces)) + r"}(\s{1})")


class Pencil:
    def __init__(self, initial_length: int=10, point_value: int=100, eraser_durability: int=10):
        self.eraser = Eraser(eraser_durability)
        self.length = initial_length
        self.sharpened_value = point_value
        self.point = point_value

    def erase(self, paper, text: str):
        self.eraser.erase(paper, text)

    def edit(self, paper, text: str):
        sub_size = len(text)
        pattern = make_re(sub_size)
        if re.search(pattern, paper.buffer):
            paper.buffer = re.sub(pattern, r"\1" + text + r"\2", paper.buffer)
        else:
            found_spaces = 0
            output = ""
            sub_pos = -1
            for c in paper.buffer:
                if c != " " and sub_pos > 0 and sub_pos < len(text) - 1:
                    output += "@"
                    sub_pos += 1
                elif c == " " and found_spaces > 0 and sub_pos <= len(text) - 1:
                    sub_pos += 1
                    output += text[sub_pos]
                    found_spaces += 1
                elif c == " " and found_spaces == 0:
                    output += c
                    found_spaces += 1
                elif c != " " and sub_pos == len(text) - 1:
                    output += c
                elif c == " " and sub_pos <= 0:
                    output += c
                else:
                    output += c
                if sub_pos == len(text) - 1:
                    found_spaces = 0
            paper.buffer = output

    def sharpen(self):
        if self.length < 1:
            return
        self.point = self.sharpened_value
        self.length -= 1

    def dull(self, char):
        if char in (' ', '\n'):
            return
        elif char in ascii_lowercase:
            self.point -= 1
        elif char in ascii_uppercase:
            self.point -= 2

    def write(self, paper, text):
        for char in text:
            if self.point > 0:
                paper.write(char)
                self.dull(char)
            else:
                paper.write(" ")
