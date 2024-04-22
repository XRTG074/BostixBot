import telebot

import BostixActions.Messaging.MessagingActions as Messaging

import BostixData.Users.UsersData as Users
import BostixData.Schools.SchoolsData as Schools
import BostixData.Schools.SchoolData as School

bot = telebot.TeleBot("МестоДляВашегоНевероятногоТокена") # - Бот 

global botLink # - Ссылка на профиль бота (Для танцев с DeepLink-ом)
botLink = "СсылкаНаВашегоНевероятногоБота"

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

# - Переменные для временного хранения перед отправкой в базу данных классов
global tempGradeName
global tempGradeLevel

# - Переменные для временного хранения перед отправкой в функцию PrintLearn
global tempLearnGrade
global tempLearnSubject
global tempLearnTopic

global joinRequests # - Короутина для последовательного вывода заявок на вступление в школу
joinRequests = None

global allowedSymbols
allowedSymbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                  '7', '8', '9']

# - Инициализация бота в другом файле

Messaging.InitBot(bot, botLink)

### - Обработчик текстовых сообщений
@bot.message_handler(content_types=["text"])
def getMessage(messageData):

    global current_menu
    global allowedSymbols
    
    # - Проверка на наличие DeepLink в сообщении

    command = messageData.text.split()

    if len(command) > 1 and current_menu == "GradesList":
        parameter = command[1]
        if parameter.split("_")[0] == "grade":
            current_menu = "GradeData"
            Messaging.showGrade(parameter.split("_")[1], messageData.from_user.id, main_message_id)

    # - Проверка на наличие аккаунта в базе данных

    if messageData.text == "/start" and current_menu == "None" and not Users.getUserData(messageData.from_user.id) is None:
        current_menu = "MainMenu"

        Messaging.MainMenu(messageData.from_user.id)

    # - Обработка сообщения "/start" от пользователя

    elif messageData.text == "/start" and current_menu == "None":
            
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

        Validness = True

        # - Проверка на наличие недопустимых символов
        
        for char in messageData.text.lower():
            if not char in allowedSymbols:
                Validness = False
                break

        if current_menu == "SignInStage2_SchoolCreateLogin" or current_menu == "SignInStage2_SchoolCreateLoginAgain_Occupied" or current_menu == "SignInStage2_SchoolCreateLoginAgain_Invalid":
            if Schools.getSchoolData(messageData.text) is None and Validness:
                global tempSchoolLogin
                tempSchoolLogin = messageData.text
                current_menu = "SignInStage2_SchoolCreateName"
                Messaging.SignInStage2(messageData.from_user.id, main_message_id, current_menu, tempRole)

            elif not "SignInStage2_SchoolCreateLoginAgain" in current_menu:
                if not Schools.getSchoolData(messageData.text) is None:
                    current_menu = "SignInStage2_SchoolCreateLoginAgain_Occupied"
                elif not Validness:
                    current_menu = "SignInStage2_SchoolCreateLoginAgain_Invalid"
            
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

    elif "GradeCreate" in current_menu:
        if current_menu == "GradeCreate_Name":
            global tempGradeName

            tempGradeName = messageData.text

            current_menu = "GradeCreate_Level"

            Messaging.NewGrade(messageData.from_user.id, main_message_id, current_menu)
        else:
            global tempGradeLevel

            try:
                if 1 <= int(messageData.text)  <= 11:
                    tempGradeLevel = messageData.text

                    current_menu = "NewGrade_Confirm"

                    Messaging.ConfrimNewGrade(messageData.from_user.id, main_message_id, tempGradeName, tempGradeLevel)
            except:
                if current_menu != "GradeCreate_LevelAgain":
                    current_menu = "GradeCreate_LevelAgain"

                    Messaging.NewGrade(messageData.from_user.id, main_message_id, current_menu)


    bot.delete_message(messageData.from_user.id, messageData.id)

### - Обработчик Inline клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def getCallback(callbackData):

    global current_menu
    global main_message_id
    global joinRequests

    if current_menu == "None":
        return
    
    if main_message_id == 0:
        main_message_id = callbackData.message.id
    
    if joinRequests is None:
        joinRequests = Messaging.JoinRequests(callbackData, main_message_id)

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

    elif callbackData.data == "learnMaterials":
        current_menu = "LearnMaterials_Grade"

        Messaging.LearnMenu(callbackData.message.chat.id, main_message_id, current_menu)
    
    elif "learn" in callbackData.data:
        if len(callbackData.data) <= 7 and not "-" in callbackData.data:
            if callbackData.data == "learn8":
                current_menu = "LearnMaterials_Subject"

                global tempLearnGrade
                tempLearnGrade = "8"
                Messaging.LearnMenu(callbackData.message.chat.id, main_message_id, current_menu)
        elif len(callbackData.data) > 7 and not "-" in callbackData.data:
            if callbackData.data == "learn8physics":
                current_menu = "LearnMaterials_Topic"

                global tempLearnSubject
                tempLearnSubject = "physics"
                Messaging.LearnMenu(callbackData.message.chat.id, main_message_id, current_menu)
        elif "-" in callbackData.data:
            if callbackData.data == "learn8physics-1":
                current_menu = "LearnMaterials_Learn"

                global tempLearnTopic
                tempLearnTopic = "-1"
                Messaging.PrintLearn(callbackData.message.chat.id, main_message_id, f'{tempLearnGrade}{tempLearnSubject}{tempLearnTopic}')



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
                if tempRole == "Teacher":
                    tempSchoolLogin = f'PendingTeacherRequest-{tempSchoolLogin}'
                else:
                    tempSchoolLogin = f'PendingRequest-{tempSchoolLogin}'
        
        Users.AddNewUser(callbackData.message.chat.id, f'{tempSurname.capitalize()}.{tempName.capitalize()}.{tempPatronymic.capitalize()}', tempSchoolLogin)
        
        if tempRole == "Principal" and not tempSchoolName is None:
            Schools.AddNewSchool(tempSchoolLogin, tempSchoolName)
            School.AddNewMemberToSchool(callbackData.message.chat.id, tempSchoolLogin, "Principal", "None")

        Messaging.MainMenu(callbackData.message.chat.id, main_message_id)


    elif callbackData.data == "checkRequests":
        current_menu = "JoinRequests"

        joinRequests.send(None)
    elif callbackData.data == "skipRequest":
        joinRequests.send(None)

    elif "acceptRequest" in callbackData.data:
        Users.replyRequestStatus(callbackData.data.split("_")[1], "Accept")
        try:
            joinRequests.send(None)
        except StopIteration:
            joinRequests = None
    elif "rejectRequest" in callbackData.data:
        Users.replyRequestStatus(callbackData.data.split("_")[1], "Reject")

        try:
            joinRequests.send(None)
        except StopIteration:
            joinRequests = None
    elif callbackData.data == "gradesList":
        current_menu = "GradesList"

        Messaging.gradesList(callbackData.message.chat.id, main_message_id)
    elif callbackData.data == "schoolMembersList":
        print()
    elif callbackData.data == "createNewGrade":
        current_menu = "GradeCreate_Name"

        Messaging.NewGrade(callbackData.message.chat.id, main_message_id, current_menu)
    elif "confirmNewGrade" in callbackData.data:
        current_menu = "GradesList"

        School.AddNewGrade(callbackData.data.split("_")[1], tempGradeName, callbackData.message.chat.id, tempGradeLevel)
        Messaging.gradesList(callbackData.message.chat.id, main_message_id)
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

        elif current_menu == "LearnMaterials_Grade":
            current_menu = "MainMenu"

            Messaging.MainMenu(callbackData.message.chat.id, main_message_id)
        if current_menu == "LearnMaterials_Subject":
            current_menu = "LearnMaterials_Grade"

            Messaging.LearnMenu(callbackData.message.chat.id, main_message_id, current_menu)
        elif current_menu == "LearnMaterials_Topic":
            current_menu = "LearnMaterials_Subject"

            Messaging.LearnMenu(callbackData.message.chat.id, main_message_id, current_menu)
        elif current_menu == "LearnMaterials_Learn":
            current_menu = "LearnMaterials_Topic"

            Messaging.LearnMenu(callbackData.message.chat.id, main_message_id, current_menu)
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


        elif current_menu == "JoinRequests":
            current_menu = "MainMenu"

            Messaging.MainMenu(callbackData.message.chat.id, main_message_id)
        elif current_menu == "GradesList":
            current_menu = "MainMenu"

            Messaging.MainMenu(callbackData.message.chat.id, main_message_id)
        elif current_menu == "GradeData":
            current_menu = "GradesList"

            Messaging.gradesList(callbackData.message.chat.id, main_message_id)
        elif "GradeCreate" in current_menu:
            if current_menu == "GradeCreate_Name":
                current_menu = "GradesList"

                Messaging.gradesList(callbackData.message.chat.id, main_message_id)
            elif current_menu == "GradeCreate_Level":
                current_menu = "GradeCreate_Name"

                Messaging.NewGrade(callbackData.message.chat.id, main_message_id, current_menu)
            elif current_menu == "GradeCreate_Level":
                current_menu = "GradeCreate_Name"

                Messaging.NewGrade(callbackData.message.chat.id, main_message_id, current_menu)
            elif current_menu == "GradeCreate_LevelAgain":
                current_menu = "GradeCreate_Name"

                Messaging.NewGrade(callbackData.message.chat.id, main_message_id, current_menu)


bot.polling(none_stop=True, interval=0) # - Ожидание сообщения от пользователя
