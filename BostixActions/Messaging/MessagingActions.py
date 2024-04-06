from telebot import types # - Библиотека для работы с крутыми штуками Telegram

import BostixData.Users.UsersData as Users # - Библиотека для работы с базой данных пользователей
import BostixData.Schools.SchoolsData as Schools # - Библиотека для работы с базой данных школ

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

# - Отправка приветственного сообщения (В случае возврата в меню)
    
def resendGreeting(callbackData, main_message_id):
  
    keyboard = types.InlineKeyboardMarkup()
    button_start = types.InlineKeyboardButton(text="НАЧАТЬ", callback_data="start")
    keyboard.add(button_start)

    bot.edit_message_text('Приветствую! Меня зовут Бостикс и я чат-бот, который готов помочь Вам с учебой или с ее организацией!,'
                     '\n\n\n<b>Учителю:</b>\n\n- Я могу быть учителем и самостоятельно проводить урок или помогать учителю с такой рутиной как перекличка, выставление оценок и отслеживание успеваемости учеников,'
                     '\n\n- Я могу составлять домашние задания, тесты и контрольные работы на основе пройденного материала. Причем индивидуальное для каждого ученика!!! (Немного случайной генерации чисел и щепотка магии)'
                     '\n\n- Помимо всего этого, Вы сможете с легкостью настраивать мои алгоритмы, составлять собственные домашние задания, тесты и контрольные работы, а также отслеживать все мои действия'
                     '\n\n<b>Ученику:</b>\n\n- Возникли трудности с пониманием какой-либо темы?'
                     'Не волнуйся, я постараюсь объяснить все как можно понятней '
                     '\n\n\nЗаинтригованны?\nТогда жмите на кнопку "НАЧАТЬ" скорее!', 
                     callbackData.message.chat.id, main_message_id, parse_mode="html", reply_markup=keyboard)


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
    
# - Отправка меню после пре-регистрации

def AfterPreSignIn(callbackData, main_message_id):
    keyboard = types.InlineKeyboardMarkup()
    button_signIn = types.InlineKeyboardButton(text="Зарегистрироваться", callback_data="signIn")
    keyboard.add(button_signIn)
    if callbackData.data == "teacher":
        button_learnMaterials = types.InlineKeyboardButton(text="Лекционные материалы", callback_data="learnMaterials")
        keyboard.add(button_learnMaterials)
    elif callbackData.data == "student":
        button_learnMaterials = types.InlineKeyboardButton(text="Лекционные материалы", callback_data="learnMaterials")
        keyboard.add(button_learnMaterials)
        button_testExams = types.InlineKeyboardButton(text="Пробные экзамены", callback_data="testExams")
        keyboard.add(button_testExams)
    button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
    keyboard.add(button_previous)
    
    # - Изменение вида меню в зависимости от выбранного на пре-регистрации (Я - учитель ИЛИ Я - ученик)

    if callbackData.data == "teacher":
        bot.edit_message_text('Отлично!\n\nЯ могу предоставить Вам лекционные материалы, которые Вы можете использовать как материал для рассказа на уроке'
                              '\nЧтобы получить к ним доступ нажмите на кнопку "Лекционные материалы"\n\nОднако это не все, что я умею. '
                              'Вы можете создать класс, в который сможете добавить всех своих учеников, чтобы присылать им домашние задания и следить за их успеваемостью, проводить уроки онлайн,'
                               ' создавать тесты и контрольные работы, индивидуальные для каждого ученика и другие вещи'
                               '\n\nНо для доступа к этому функционалу Вам необходимо зарегистрироваться'
                               '\nНажмите на кнопку "Зарегистрироваться" ниже и создайте аккаунт',
                               callbackData.message.chat.id, main_message_id, parse_mode="html",reply_markup=keyboard)
    elif callbackData.data == "student":
        bot.edit_message_text('Отлично!\n\nЯ могу предоставить Вам лекционные материалы, которые Вы можете использовать как шпаргалку при выполнении домашних заданий'
                              '\nЧтобы получить к ним доступ нажмите на кнопку "Лекционные материалы"'
                              '\n\nВы также можете проверить свои знания, пройдя тест или конрольную работу, которую я сгенерирую для Вас. '
                              'Просто нажмите на кнопку "Пробные экзамены" и выберите необходимый вам предмет и класс'
                              '\n\nОднако это не все, что я умею. Если Ваш учитель создал класс, Вы можете присоединиться к нему и получать знания!'
                              '\n\nНо для доступа к этому функционалу Вам необходимо зарегистрироваться\nНажмите на кнопку "Зарегистрироваться" ниже и создайте аккаунт',
                              callbackData.message.chat.id, main_message_id, parse_mode="html",reply_markup=keyboard)
    else:
        bot.edit_message_text('Отлично!\n\nЯ могу предоставить Вам обширный функционал для управления школы. '
                              'Контролируйте школу, классы, действия учителей, отслеживайте "проблемных учеников", создавайте массовые рассылки важной информации и многое другое'
                              '\n\nНо для доступа к этому функционалу Вам необходимо зарегистрироваться'
                              '\nНажмите на кнопку "Зарегистрироваться" ниже и создайте аккаунт',
                              callbackData.message.chat.id, main_message_id, parse_mode="html",reply_markup=keyboard)
        
# - Первый этап регистрации

def SignInStage1(chat_id, main_message_id, current_menu):

    keyboard = types.InlineKeyboardMarkup()
    button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
    keyboard.add(button_previous)

    # - Запрос фамилии пользователя
  
    if current_menu == "SignInStage1_Surname":
        bot.edit_message_text("Поехали!\n\nПожалуйста напишите мне Вашу <b>настоящую</b> Фамилию:",
                              chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)

    # - Запрос имени пользователя

    elif current_menu == "SignInStage1_Name":
        bot.edit_message_text("Хорошо\n\nТеперь напишите мне Ваше <b>настоящее</b> Имя:",
                              chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)

    # - Запрос отчества пользователя

    elif current_menu == "SignInStage1_Patronymic":
      
        bot.edit_message_text("И еще один вопрос\n\nПожалуйста напишите мне Ваше <b>настоящее</b> Отчество:",
                              chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)

# - Подтверждение первого этапа регистрации

def ConfirmSignInStage1(surname, name, patronymic, chat_id, main_message_id):
    keyboard = types.InlineKeyboardMarkup()
    button_confirm = types.InlineKeyboardButton(text="Да, все верно", callback_data="confirmSignInStage1")
    keyboard.add(button_confirm)
    button_edit = types.InlineKeyboardButton(text="Нет, мне нужно кое-что изменить", callback_data="editSignInStage1")
    keyboard.add(button_edit)
    button_previous = types.InlineKeyboardButton(text="Назад", callback_data="previous")
    keyboard.add(button_previous)

    bot.edit_message_text(f"Вас зовут: <b>{surname.capitalize()} {name.capitalize()} {patronymic.capitalize()}</b>, все верно?",
                          chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)

# - Второй этап регистрации

def SignInStage2(chat_id, main_message_id, current_menu, role):
    print(current_menu)
    keyboard = types.InlineKeyboardMarkup()

    if current_menu == "SignInStage2_SchoolAdd":
        if role == "Principal":
            button_createSchool = types.InlineKeyboardButton(text="Создать школу", callback_data="createSchool")
            keyboard.add(button_createSchool)

        button_linkSchool = types.InlineKeyboardButton(text="Привязать школу", callback_data="linkSchool")
        keyboard.add(button_linkSchool)
        button_skip = types.InlineKeyboardButton(text="Пропустить этот шаг", callback_data="skipSchoolAdd")
        keyboard.add(button_skip)

        button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
        keyboard.add(button_previous)

        if role == "Teacher":
            bot.edit_message_text('Окей, тогда продолжаем:\n\n\nЕсли Ваш директор/управляющее лицо создало электронную школу в моей базе данных, '
                                  'Вы можете присоединиться к ней введя ее уникальный <b>логин</b>, который можно узнать у одного из лиц, '
                                  'имеющих к нему доступ\n\nПосле того, как Вашу заявку одобрят, и подтвердят Ваш статус учителя, '
                                  'Вы сможете создать класс и добавить туда Ваших учеников'
                                  '\n\nЕсли у Вас есть <b>логин</b> Вашей школы, нажмите на кнопку "Привязать школу"'
                                  '\n\nВ противном случае нажмите на кнопку "Пропустить этот шаг"\nВы сможете создать/привязать школу позже, в настройках Вашего профиля',
                                    chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)
        elif role == "Student":
            bot.edit_message_text('Окей, тогда продолжаем:\n\n\nЕсли Ваш директор/управляющее лицо создало электронную школу в моей базе данных, '
                                  'Вы можете присоединиться к ней введя ее уникальный <b>логин</b>, который можно узнать у одного из лиц, имеющих к нему доступ'
                                  '\n\nПосле того, как Вашу заявку одобрят, Ваш учитель/классный руководитель сможет добавить Вас в Ваш класс'
                                  '\n\nЕсли у Вас есть <b>логин</b> Вашей школы, нажмите на кнопку "Привязать школу"'
                                  '\n\nВ противном случае нажмите на кнопку "Пропустить этот шаг"'
                                  '\nВы сможете создать/привязать школу позже, в настройках Вашего профиля',
                                  chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)
        else:
            bot.edit_message_text('Окей, тогда продолжаем:\n\n\nСейчас Вы можете создать свою школу, куда Вы добавите всех учителей, '
                                  'а они в свою очередь всех своих учеников\n\nВы можете создать школу прямо сейчас - это не сложно!'
                                  '\nНажмите на кнопку "Создать школу", и Я все Вам объясню\n\nБыть может, кто-то из важных лиц Вашей школы уже создал ее?'
                                   ' - Тогда Вы можете присоединиться к ней, введя ее уникальный <b>логин</b>, который Вы можете узнать у одного из лиц, имеющих к нему доступ'
                                   '\n\nЕсли у Вас есть <b>логин</b> Вашей школы, нажмите на кнопку "Привязать школу"'
                                   '\n\nВ противном случае нажмите на кнопку "Пропустить этот шаг"\nВы сможете создать/привязать школу позже, в настройках Вашего профиля',
                                   chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)

    elif current_menu == "SignInStage2_SchoolCreateLogin":
        button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
        keyboard.add(button_previous)
        bot.edit_message_text('Тогда вперед!\n\nПридумайте <b>логин</b> Вашей школы'
                             '\nОн будет использоваться как второе имя Вашей школы и для ряда других вещей'
                             '\n\nНапишите мне <b>логин</b> Вашей школы:',
                             chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)
        
    elif current_menu == "SignInStage2_SchoolCreateLoginAgain":
        button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
        keyboard.add(button_previous)
        bot.edit_message_text('К сожалению этот невероятный <b>логин</b> уже занят((('
                              '\n\nПридумайте и напишите мне <b>логин</b> еще раз:',
                                chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)
        
    elif current_menu == "SignInStage2_SchoolCreateName":
        button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
        keyboard.add(button_previous)
        bot.edit_message_text("И последний рывок:\n\nТеперь напишите мне название Вашей школы", 
                                  chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)
    
    elif current_menu == "SignInStage2_SchoolLink":
        button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
        keyboard.add(button_previous)
        bot.edit_message_text('Тогда вперед!\n\nНапишите мне <b>логин</b> школы в которую Вы хотите вступить:',
                              chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)

    elif current_menu == "SignInStage2_SchoolLinkAgain":
        button_previous = types.InlineKeyboardButton(text="Вернуться к предыдущему шагу", callback_data="previous")
        keyboard.add(button_previous)
        bot.edit_message_text('Я не смог обнаружить школы с таким <b>логином</b>\n\n'
        'Напишите мне <b>логин</b> Вашей школы еще раз:',
        chat_id, main_message_id, parse_mode="html", reply_markup=keyboard)

# - Подтверждение второго этапа регистрации

def ConfirmSignInStage2(schoolLogin, messageData, main_message_id, role, schoolName='ЗдесьБуквальноНичегоНету'):
    keyboard = types.InlineKeyboardMarkup()
    button_confirm = types.InlineKeyboardButton(text="Да, все верно", callback_data="confirmSignInStage2")
    keyboard.add(button_confirm)
    button_edit = types.InlineKeyboardButton(text="Нет, мне нужно кое-что изменить", callback_data="editSignInStage2")
    keyboard.add(button_edit)
    button_previous = types.InlineKeyboardButton(text="Назад", callback_data="previous")
    keyboard.add(button_previous)

    if role == "Principal" and Schools.getSchoolData(schoolLogin) is None:
        bot.edit_message_text(f"Я создам школу <b>{schoolName},</b> которая также будет известна под логином <b>{schoolLogin}</b>\n\nВсе верно?",
                              messageData.from_user.id, main_message_id, parse_mode="html", reply_markup=keyboard)
    elif role == "Teacher":
        bot.edit_message_text(f'Я отправлю заявку на вступление (и получение роли учителя) в школу под названием <b>{Schools.getSchoolData(schoolLogin)[1]}</b>, '
                              f'также известную как <b>{schoolLogin}</b>'
                              '\n\nВсе верно?',
                                messageData.from_user.id, main_message_id, parse_mode="html", reply_markup=keyboard)
    else:
        bot.edit_message_text(f'Я отправлю заявку на вступление в школу под названием <b>{Schools.getSchoolData(schoolLogin)[1]}</b>, '
                              f'также известную как <b>{schoolLogin}</b>'
                              '\n\nВсе верно?',
                              messageData.from_user.id, main_message_id, parse_mode="html", reply_markup=keyboard)

# - Подтверждение регистрации

def ConfirmSignIn(callbackData, main_message_id):
    keyboard = types.InlineKeyboardMarkup()
    button_finish = types.InlineKeyboardButton(text="Закончить регистрацию", callback_data="finishSignIn")
    keyboard.add(button_finish)
    button_previous = types.InlineKeyboardButton(text="Отменить регистрацию", callback_data="previous")
    keyboard.add(button_previous)
    
    bot.edit_message_text('Вот и все! Ваш аккаунт почти создан\n\n'
    'Дополнительную информацию о Вас Вы сможете добавить к Вашему профилю в настройках в любое время'
    '\n\nДля входа в Ваш аккаунт будет использоваться <b>Ваш аккаунт Telegram</b>'
    '\n\nЧтобы завершить регистрацию и создать аккаунт, нажмите на кнопку "Закончить регистрацию"',
    callbackData.message.chat.id, main_message_id, parse_mode="html", reply_markup=keyboard)
