import telebot

import BostixActions.Messaging.MessagingActions as Messaging

bot = telebot.TeleBot("МестоДляОченьКрутогоТокена") # - Бот

main_message_id = 0 # ID главного сообщения, где будет происходить все

current_menu = "None" # - Текущее меню бота


# - Инициализация бота в другом файле

Messaging.InitBot(bot)

### - Обработчик текстовых сообщений
@bot.message_handler(content_types=["text"])
def getMessage(messageData):

    global current_menu
        
    # - Обработка сообщения "/start" от пользователя

    if messageData.text == "/start" and current_menu == "None":
            
            current_menu = "Greeting"

            if main_message_id == 0:
                  Messaging.sendGreeting(messageData)

### - Обработчик Inline клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def getCallback(callbackData):

    global current_menu

    if current_menu == "None":
        return

    global main_message_id
    
    if main_message_id == 0:
        main_message_id = callbackData.message.id

    # - Обработка нажатия кнопки "НАЧАТЬ"

    if callbackData.data == "start":
        current_menu = "PreSignIn"

        Messaging.StartPreSignIn(callbackData, main_message_id)
    
    # - Обработка нажатия кнопки "Я - учитель, "Я - ученик" или "Я - директор школы"

    elif callbackData.data == "teacher" or callbackData.data == "student" or callbackData.data == "principal":
        global tempRole # - Временная переменная школьного статуса пользователя

        if callbackData.data == "teacher":
            tempRole = "Teacher"
        elif callbackData.data == "student":
            tempRole = "Student"
        else:
            tempRole = "Principal"

        current_menu = "AfterPreSignIn"

        Messaging.AfterPreSignIn(callbackData, main_message_id)


bot.polling(none_stop=True, interval=0) # - Ожидание сообщения от пользователя