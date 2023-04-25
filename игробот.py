from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from random import randint
from telegram import ReplyKeyboardMarkup

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
a = randint(1, 10)


async def start(update, context):
    user = update.effective_user
    # начало общения с ботом
    context.user_data['try_'] = 5
    context.user_data['mi'] = 1
    context.user_data['ma'] = 10
    context.user_data['count'] = 1
    reply_keyboard3 = [['да', 'нет']]
    markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)
    await update.message.reply_html(
        # приветственная фраза бота
        rf'Привет {user.mention_html()}! Я игробот. Хотите поиграть в игру "Угадай число"?',
        reply_markup=markup3)
    # переход к первому действию
    return 1


async def first_response(update, context):
    # первый ответ
    answer = update.message.text

    if answer == 'Да' or answer == 'да':
        # действия при ответе "да"
        reply_keyboard4 = [['я', 'бот']]
        markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True)
        await update.message.reply_text(
            f'Давайте начнем! Кто будет угадывать? Напишите: "я" или "бот".',
            reply_markup=markup4)
        # переход ко второму действию
        return 2

    elif answer == 'Нет' or answer == 'нет':
        # действия при ответе "нет"
        reply_keyboard5 = [['/start']]
        markup5 = ReplyKeyboardMarkup(reply_keyboard5, one_time_keyboard=True)
        await update.message.reply_text(
            "Всего доброго!", reply_markup=markup5)
        return ConversationHandler.END

        # неправильный ответ
    reply_keyboard3 = [['да', 'нет']]
    markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)
    await update.message.reply_text(
        f'Я не понимаю вас. Напишите "Да" или "Нет".', reply_markup=markup3)


async def second_response(update, context):
    answer = update.message.text

    if answer == 'бот':
        # действия при ответе "бот"
        reply_keyboard6 = [['да']]
        markup6 = ReplyKeyboardMarkup(reply_keyboard6, one_time_keyboard=True)
        await update.message.reply_text(
            f'Загадайте число от 1 до 10. Напишите "да", когда будете готовы.', reply_markup=markup6)
        # переход к трьетьему действию
        return 3

    elif answer == 'я':
        # действия при ответе "я"
        # выбор числа от 1 до 10 ботом
        reply_keyboard2 = [['1', '2', '3', '4', '5'], ['6', '7', '8', '9', '10']]
        markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
        await update.message.reply_text(
            f'Я загадал число от 1 до 10. Попробуйте угадать.',
            reply_markup=markup2)
        # переход к четвертому действию
        return 4

    # неправильный ответ
    reply_keyboard4 = [['я', 'бот']]
    markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True)
    await update.message.reply_text(
        f'Я не понимаю вас. Напишите "я" или "бот".', reply_markup=markup4)


async def third_response(update, context):
    answer = update.message.text
    mi = context.user_data['mi']
    ma = context.user_data['ma']
    count = context.user_data['count'] 
    try_ = context.user_data['try_']

    if answer == 'да':
        reply_keyboard = [['больше', 'меньше'], ['верно']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_html(
            f'Это число {try_}? Напишите "верно", "больше" или "меньше"',
            reply_markup=markup)
        return 3

    elif answer == 'верно':
        reply_keyboard3 = [['да', 'нет']]
        markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)
        await update.message.reply_text(
            f'Ура! Я победил! Хотите сыграть еще раз?', reply_markup=markup3)
        return 1

    elif answer == 'больше':
        reply_keyboard = [['больше', 'меньше'], ['верно']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        mi = try_
        try_ = try_ + ((ma - mi) // 2)
        await update.message.reply_text(
            f'Это число {try_}?',
            reply_markup=markup)
        context.user_data.clear()
        context.user_data['try_'] = try_
        context.user_data['mi'] = mi
        context.user_data['ma'] = ma
        context.user_data['count'] = 2
        return 3

    elif answer == 'меньше':
        reply_keyboard = [['больше', 'меньше'], ['верно']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        ma = try_
        try_ = try_ - ((ma - mi) // 2)
        await update.message.reply_text(
            f'Это число {try_}?',
            reply_markup=markup)
        context.user_data.clear()
        context.user_data['try_'] = try_
        context.user_data['ma'] = ma
        context.user_data['mi'] = mi
        context.user_data['count'] = 2
        return 3

    # неправильный ответ
    if count == 1:
        reply_keyboard6 = [['да']]
        markup6 = ReplyKeyboardMarkup(reply_keyboard6, one_time_keyboard=True)
        await update.message.reply_text(
            f'Я не понимаю вас. Загадайте число от 1 до 10. Напишите "да", когда будете готовы.', reply_markup=markup6)
        context.user_data.clear()
        context.user_data['count'] = 2
        context.user_data['try_'] = try_
        context.user_data['mi'] = mi
        context.user_data['ma'] = ma
    elif count == 2:
        reply_keyboard = [['больше', 'меньше'], ['верно']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            f'Я не понимаю вас. Это число {try_}? Напишите "верно", "больше" или "меньше"',
            reply_markup=markup)


async def fourth_response(update, context):
    answer = update.message.text

    if answer in numbers:
        reply_keyboard2 = [['1', '2', '3', '4', '5'], ['6', '7', '8', '9', '10']]
        markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
        if a > int(answer):
            await update.message.reply_text(f'больше', reply_markup=markup2)
            return 4
        elif a < int(answer):
            await update.message.reply_text(f'меньше', reply_markup=markup2)
            return 4
        else:
            reply_keyboard3 = [['да', 'нет']]
            markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)
            await update.message.reply_text(
                f'Верно! Вы победили! Хотите сыграть еще раз?', reply_markup=markup3)
            return 1

    reply_keyboard2 = [['1', '2', '3', '4', '5'], ['6', '7', '8', '9', '10']]
    markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
    # неправильный ответ
    await update.message.reply_text(
        f'Я не понимаю вас. Попробуйте угадать, какое число от 1 до 10 я загадал.', reply_markup=markup2)


async def stop(update, context):
    reply_keyboard5 = [['/start']]
    markup5 = ReplyKeyboardMarkup(reply_keyboard5, one_time_keyboard=True)
    await update.message.reply_text(
        "Всего доброго!", reply_markup=markup5)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response)],
        4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response)]
    },

    fallbacks=[CommandHandler('stop', stop)]
)


def main():
    application = Application.builder().token('6091047516:AAFx3xUHUTUd281ywZyAnN9v6i5y7vpONhg').build()
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
