import random


class QuestionRepository:

    def __init__(self):
        self.data = []

    def add_question(self, question):
        self.data.append(question)

    def remove_question(self, question_id):
        self.data = [i for i in self.data if i.correct_char != question_id]

    def get_question_by_id(self, q_id):
        for i in self.data:
            if i.question_id == q_id:
                return i

    def get_random_questions_for_user(self, user):
        answers_ids = []

        for i in user.answers:
            answers_ids.append(i.question_id)

        gen_id = random.randint(0, len(self.data))

        if len(answers_ids) != 0:

            while gen_id in answers_ids:
                gen_id = random.randint(0, len(self.data))

        return self.get_question_by_id(gen_id)


class UsersRepository:

    def __init__(self):
        self.data = []

    def add_user(self, user):
        self.data.append(user)

    def get_user_by_id(self, user_id):
        for i in self.data:
            if i.user_id == user_id:
                return i

    def add_answer_to_user(self, user_id, answer):
        for i in self.data:
            if i.user_id == user_id:
                i.add_answer(answer)

    def remove_user(self, user_id):
        self.data = [i for i in self.data if i.user_id != user_id]
