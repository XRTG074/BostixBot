import telebot

import BostixActions.Messaging.MessagingActions as Messaging

bot = telebot.TeleBot("МестоДляОченьКрутогоТокена") # - Бот

main_message_id = 0 # ID главного сообщения, где будет происходить все

current_menu = "None" # - Текущее меню бота

# - Переменные для временного хранения перед отправкой в базу данных пользователей
global tempSurname
global tempName
global tempPatronymic


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
    
    # - Получение фамилии, имени и отчества

    elif "SignInStage1" in current_menu:
        if current_menu == "SignInStage1_Surname":
            tempSurname = messageData.text
          
            current_menu = "SignInStage1_Name"

            Messaging.SignInStage1(messageData.from_user.id, main_message_id, current_menu)
        elif current_menu == "SignInStage1_Name":
            tempName = messageData.text
          
            current_menu = "SignInStage1_Patronymic"

            Messaging.SignInStage1(messageData.from_user.id, main_message_id, current_menu)
        elif current_menu == "SignInStage1_Patronymic":
            tempPatronymic = messageData.text

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
    
    # - Обработка нажатия кнопки "Зарегистрироваться"
  
    elif callbackData.data == "signIn":
        current_menu = "SignInStage1_Surname"

        Messaging.SignInStage1(callbackData.message.chat.id, main_message_id, current_menu)


bot.polling(none_stop=True, interval=0) # - Ожидание сообщения от пользователя