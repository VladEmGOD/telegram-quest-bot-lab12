import json

from Repositories import UsersRepository
from Models import Answer, User
from Questions import question_repository
import telebot
import config
import pytz


QUESTION_COUNT = 10

bot = telebot.TeleBot(config.TOKEN)

users_repo = UsersRepository()


def generate_question_buttons(question_id):
    buttons = telebot.types.InlineKeyboardMarkup(row_width=4)
    btn_1 = telebot.types.InlineKeyboardButton('A', callback_data=json.dumps(Answer(question_id, "A").__dict__))
    btn_2 = telebot.types.InlineKeyboardButton('B', callback_data=json.dumps(Answer(question_id, "B").__dict__))
    btn_3 = telebot.types.InlineKeyboardButton('C', callback_data=json.dumps(Answer(question_id, "C").__dict__))
    btn_4 = telebot.types.InlineKeyboardButton('D', callback_data=json.dumps(Answer(question_id, "D").__dict__))
    buttons.add(btn_1, btn_2, btn_3, btn_4)
    return buttons


def calculate_res(answers):
    res = ""
    correct_answers = 0
    for i in answers:
        question = question_repository.get_question_by_id(i.question_id)
        if question.correct_char == i.answer_char:
            res += f"question #{question.question_id} - {1}\n"
            correct_answers += 1
        else:
            res += f"question #{question.question_id} - {0}\n"

    res += f"mark: {correct_answers}/10"
    return res


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'I HATE SESSIA!!!!!!!!\n😡 😡 😡 😡 😡 🤬 🤬 🤬 🤬 🤬 🤬')
    user = User(user_id=message.chat.id)
    users_repo.add_user(user)
    question = question_repository.get_random_questions_for_user(user)
    bot.send_message(message.chat.id, question.text, reply_markup=generate_question_buttons(question.question_id))


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    answer_json = json.loads(call.data)
    answer = Answer(answer_json["question_id"], answer_json["answer_char"])

    user_id = call.message.chat.id
    user = users_repo.get_user_by_id(user_id)

    if user:
        if len(user.answers) >= QUESTION_COUNT:
            result = calculate_res(user.answers)
            users_repo.remove_user(user.user_id)
            bot.send_message(chat_id=user_id, text=result)
        else:
            users_repo.add_answer_to_user(user.user_id, answer)
            question = question_repository.get_random_questions_for_user(user)
            bot.send_message(call.message.chat.id, question.text,
                             reply_markup=generate_question_buttons(question.question_id))


bot.polling(none_stop=True)
