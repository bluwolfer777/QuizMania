import random
class Question:
    def __init__(self, text, answers, rightAnswer, difficulty):
        self.text = text
        self.answers = answers
        self.rightAnswer = rightAnswer
        self.difficulty = difficulty

    def getMixedAswers(self):
        random.shuffle(self.answers)
        return self.answers