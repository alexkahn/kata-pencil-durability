class Eraser:
    def __init__(self, durability=100):
        self.durability = durability

    def erase(self, paper, text):
        if self.durability > 0:
            if self.cost(text) <= self.durability:
                self.remove_text(paper, text)
                self.durability -= self.cost(text)
            else:
                self.remove_text(paper, text[-self.durability:])


    def cost(self, text):
        costly = text.replace(' ', '')
        return len(costly)

    def remove_text(self, paper, text):
        rep = ' ' * len(text)
        paper.buffer = paper.buffer[::-1].replace(text[::-1], rep, 1)[::-1]
