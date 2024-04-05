from telebot import types # - Библиотека для работы с крутыми штуками Telegram


# - Инициализация бота

def InitBot(_bot):
    global bot
    bot = _bot

# - Отправка приветственного сообщения

def sendGreeting(messageData):
    keyboard = types.InlineKeyboardMarkup()
    button_start = types.InlineKeyboardButton(text="НАЧАТЬ", callback_data="start")
    keyboard.add(button_start)

    bot.send_message(messageData.from_user.id, 'Приветствую! Меня зовут Бостикс и я чат-бот, который готов помочь Вам с учебой или с ее организацией!,'
                     '\n\n\n<b>Учителю:</b>\n\n- Я могу быть учителем и самостоятельно проводить урок или помогать учителю с такой рутиной как перекличка, выставление оценок и отслеживание успеваемости учеников,'
                     '\n\n- Я могу составлять домашние задания, тесты и контрольные работы на основе пройденного материала. Причем индивидуальное для каждого ученика!!! (Немного случайной генерации чисел и щепотка магии)'
                     '\n\n- Помимо всего этого, Вы сможете с легкостью настраивать мои алгоритмы, составлять собственные домашние задания, тесты и контрольные работы, а также отслеживать все мои действия'
                     '\n\n<b>Ученику:</b>\n\n- Возникли трудности с пониманием какой-либо темы?'
                     'Не волнуйся, я постараюсь объяснить все как можно понятней '
                     '\n\n\nЗаинтригованны?\nТогда жмите на кнопку "НАЧАТЬ" скорее!', 
                     parse_mode="html", reply_markup=keyboard)

# - Начало пре-регистрации

def StartPreSignIn(callbackData, main_message_id):
    keyboard = types.InlineKeyboardMarkup()
    button_teacher = types.InlineKeyboardButton(text="Я - учитель", callback_data="teacher")
    button_student = types.InlineKeyboardButton(text="Я - ученик", callback_data="student")
    keyboard.add(button_teacher, button_student)
    button_principal = types.InlineKeyboardButton(text="Я - директор школы", callback_data="principal")
    keyboard.add(button_principal)
    button_exit = types.InlineKeyboardButton(text="Вернуться в меню", callback_data="previous")
    keyboard.add(button_exit)

    bot.edit_message_text("Давайте начинать!\n\nВы <b>учитель</b> или <b>ученик</b>?",
                          callbackData.message.chat.id, main_message_id, parse_mode="html", reply_markup=keyboard)
