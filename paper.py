class Paper:
    def __init__(self, text: str=""):
        self.buffer: str = text

    def write(self, text: str):
        self.buffer += text
