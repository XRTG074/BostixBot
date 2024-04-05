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


bot.polling(none_stop=True, interval=0) # - Ожидание сообщения от пользователя