import pytest

from eraser import Eraser
from pencil import Pencil
from paper import Paper


def test_writing():
    paper = Paper("She sells sea shells")
    pencil = Pencil()
    pencil.write(paper, " by the sea shore")
    assert paper.buffer == "She sells sea shells by the sea shore"


@pytest.mark.parametrize("char,value", [
    (" ", 100),
    ("\n", 100),
    ("a", 99),
    ("A", 98),
])
def test_dulling(char, value):
    paper = Paper()
    pencil = Pencil()
    pencil.write(paper, char)
    assert pencil.point == value


@pytest.mark.parametrize("text,output_value", [
    ("text", "text"),
    ("Text", "Tex "),
])
def test_dulling_with_writing(text, output_value):
    paper = Paper()
    pencil = Pencil(point_value=4)
    pencil.write(paper, text)
    assert paper.buffer == output_value


def test_sharpening():
    pencil = Pencil(initial_length=1000, point_value=10)
    [pencil.dull("C") for _ in range(5)]
    assert pencil.point == 0
    pencil.sharpen()
    assert pencil.point == 10


def test_sharpening_when_length_is_low():
    pencil = Pencil(1)
    assert pencil.length == 1
    pencil.sharpen()
    assert pencil.length == 0


@pytest.mark.parametrize("input_text,erase_text,output_text", [
    ("How much wood would a woodchuck chuck if a woodchuck could chuck wood?", "chuck", "How much wood would a woodchuck chuck if a woodchuck could       wood?")
])
def test_eraser(input_text, erase_text, output_text):
    paper = Paper(input_text)
    eraser = Eraser()
    eraser.erase(paper, erase_text)
    assert paper.buffer == output_text


def test_eraser_erases_the_next_occurence_of_text():
    initial_text = "How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
    erase_text = "chuck"
    paper = Paper(initial_text)
    eraser = Eraser()
    eraser.erase(paper, erase_text)
    eraser.erase(paper, erase_text)
    expected_text = "How much wood would a woodchuck chuck if a wood      could       wood?"
    assert paper.buffer == expected_text


def test_eraser_can_run_out():
    paper = Paper("Buffalo Bill")
    eraser = Eraser(3)
    eraser.erase(paper, "Bill")
    assert paper.buffer == "Buffalo B   "


@pytest.mark.parametrize("initial_text,new_text,output", [
    ("An       a day keeps the doctor away", "onion", "An onion a day keeps the doctor away"),
    ("An       a day keeps the doctor away", "artichoke", "An artich@k@ay keeps the doctor away"),
])
def test_editing_replaces_text(initial_text, new_text, output):
    paper = Paper(initial_text)
    pencil = Pencil()
    pencil.edit(paper, new_text)
    assert paper.buffer == output
