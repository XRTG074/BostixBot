import telebot

import BostixActions.Messaging.MessagingActions as Messaging

import BostixData.Users.UsersData as Users
import BostixData.Schools.SchoolsData as Schools

bot = telebot.TeleBot("МестоДляОченьКрутогоТокена") # - Бот

main_message_id = 0 # ID главного сообщения, где будет происходить все

current_menu = "None" # - Текущее меню бота

# - Переменные для временного хранения перед отправкой в базу данных пользователей
global tempSurname
global tempName
global tempPatronymic

# - Переменные для временного хранения перед отправкой в базу данных школ
global tempSchoolLogin
global tempSchoolName
tempSchoolName = None

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
            global tempSurname
            tempSurname = messageData.text
          
            current_menu = "SignInStage1_Name"

            Messaging.SignInStage1(messageData.from_user.id, main_message_id, current_menu)
        elif current_menu == "SignInStage1_Name":
            global tempName
            tempName = messageData.text
          
            current_menu = "SignInStage1_Patronymic"

            Messaging.SignInStage1(messageData.from_user.id, main_message_id, current_menu)
        elif current_menu == "SignInStage1_Patronymic":
            global tempPatronymic
            tempPatronymic = messageData.text

            current_menu = "SignInStage1_Confirm"

            Messaging.ConfirmSignInStage1(tempSurname, tempName, tempPatronymic, messageData.from_user.id, main_message_id)

    # - Получение логина и названия школы

    elif "SignInStage2_School" in current_menu:
        if current_menu == "SignInStage2_SchoolCreateLogin" or current_menu == "SignInStage2_SchoolCreateLoginAgain":
            if Schools.getSchoolData(messageData.text) is None:
                global tempSchoolLogin
                tempSchoolLogin = messageData.text
                current_menu = "SignInStage2_SchoolCreateName"

            if current_menu != "SignInStage2_SchoolCreateLoginAgain":
                if not Schools.getSchoolData(messageData.text) is None:
                    current_menu = "SignInStage2_SchoolCreateLoginAgain"
                Messaging.SignInStage2(messageData.from_user.id, main_message_id, current_menu, tempRole)
        elif current_menu == "SignInStage2_SchoolCreateName":
            current_menu = "SignInStage2_Confirm"

            global tempSchoolName
            tempSchoolName = messageData.text

            Messaging.ConfirmSignInStage2(tempSchoolLogin, messageData, main_message_id, tempRole, tempSchoolName)
        elif current_menu == "SignInStage2_SchoolLink" or current_menu == "SignInStage2_SchoolLinkAgain":
            if not Schools.getSchoolData(messageData.text) is None:
                tempSchoolLogin = messageData.text

                current_menu = "SignInStage2_Confirm"
            if current_menu != "SignInStage2_SchoolLinkAgain":
                if Schools.getSchoolData(messageData.text) is None:
                    current_menu = "SignInStage2_SchoolLinkAgain"
                    Messaging.SignInStage2(messageData.from_user.id, main_message_id, current_menu, tempRole)
                else:
                    Messaging.ConfirmSignInStage2(tempSchoolLogin, messageData, main_message_id, tempRole)

    bot.delete_message(messageData.from_user.id, messageData.id)

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
    
    # - Начало второго этапа регистрации

    elif callbackData.data == "confirmSignInStage1":
        current_menu = "SignInStage2_SchoolAdd"

        Messaging.SignInStage2(callbackData.message.chat.id, main_message_id, current_menu, tempRole)

    # - Обработка нажатия кнопки "Создать школу"

    elif callbackData.data == "createSchool":
        current_menu = "SignInStage2_SchoolCreateLogin"

        Messaging.SignInStage2(callbackData.message.chat.id, main_message_id, current_menu, tempRole)

    elif callbackData.data == "confirmSignInStage2":
        current_menu = "ConfirmSignIn"

        Messaging.ConfirmSignIn(callbackData, main_message_id)

    elif callbackData.data == "linkSchool":
        current_menu = "SignInStage2_SchoolLink"

        Messaging.SignInStage2(callbackData.message.chat.id, main_message_id, current_menu, tempRole)

    elif callbackData.data == "skipSchoolLink":
        current_menu = "ConfirmSignIn"

        Messaging.ConfirmSignIn(callbackData, main_message_id)
    
    elif callbackData.data == "finishSignIn":
        global tempSchoolLogin
        
        current_menu = "MainMenu"
        if not tempSchoolLogin is None:
            if not Schools.getSchoolData(tempSchoolLogin) is None:
                tempSchoolLogin = f'PendingRequest-{tempSchoolLogin}'
        
        Users.AddNewUser(callbackData.message.chat.id, f'{tempSurname}.{tempName}.{tempPatronymic}', tempSchoolLogin)
        
        if tempRole == "Principal" and not tempSchoolName is None:
            Schools.AddNewSchool(tempSchoolLogin, tempSchoolName)
    elif callbackData.data == "previous":
        if current_menu == "PreSignIn":
            current_menu = "Greeting"

            Messaging.resendGreeting(callbackData, main_message_id)
        elif current_menu == "AfterPreSignIn":
            current_menu = "PreSignIn"

            Messaging.StartPreSignIn(callbackData, main_message_id)
        elif "SignInStage1" in current_menu and current_menu != "SignInStage1_Confirm":
            callbackData.data = tempRole.lower()
            if current_menu == "SignInStage1_Surname":
                current_menu = "AfterPreSignIn"

                Messaging.AfterPreSignIn(callbackData, main_message_id)
            elif current_menu == "SignInStage1_Name":
                current_menu = "SignInStage1_Surname"

                Messaging.SignInStage1(callbackData.message.chat.id, main_message_id, current_menu)
            else:
                current_menu = "SignInStage1_Name"

                Messaging.SignInStage1(callbackData.message.chat.id, main_message_id, current_menu)
        elif current_menu == "SignInStage1_Confirm":
            current_menu = "AfterPreSignIn"

            Messaging.AfterPreSignIn(callbackData, main_message_id)
        elif "SignInStage2_School" in current_menu and current_menu != "SignInStage2_Confirm":
            if current_menu == "SignInStage2_SchoolAdd":
                current_menu = "SignInStage1_Confirm"

                Messaging.ConfirmSignInStage1(tempSurname, tempName, tempPatronymic, callbackData.message.chat.id, main_message_id)
            elif current_menu == "SignInStage2_SchoolCreateLogin" or current_menu == "SignInStage2_SchoolCreateLogin":
                current_menu = "SignInStage2_SchoolAdd"

                Messaging.SignInStage2(callbackData.message.chat.id, main_message_id, current_menu, tempRole)
            elif current_menu == "SignInStage2_SchoolLink" or current_menu == "SignInStage2_SchoolLinkAgain":
                current_menu = "SignInStage2_SchoolAdd"

                Messaging.SignInStage2(callbackData.message.chat.id, main_message_id, current_menu, tempRole)
            elif current_menu == "SignInStage2_SchoolCreateName":
                current_menu = "SignInStage2_SchoolCreateLogin"

                Messaging.SignInStage2(callbackData.message.chat.id, main_message_id, current_menu, tempRole)
        elif current_menu == "SignInStage2_Confirm":
                current_menu = "SignInStage2_SchoolAdd"

                Messaging.SignInStage2(callbackData.message.chat.id, main_message_id, current_menu, tempRole)
        elif current_menu == "ConfirmSignIn":
            current_menu = "AfterPreSignIn"

            Messaging.StartPreSignIn(callbackData, main_message_id)


bot.polling(none_stop=True, interval=0) # - Ожидание сообщения от пользователя