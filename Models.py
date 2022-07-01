class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.answers = []

    def add_answer(self, answer):
        self.answers.append(answer)


class Question:
    def __init__(self, q_id, text, correct_char):
        self.question_id = q_id
        self.text = text
        self.correct_char = correct_char


class Answer:
    def __init__(self, question_id, answer_char):
        self.question_id = question_id
        self.answer_char = answer_char
