import sqlite3 # - Библиотека базы данных

import BostixData.Schools.SchoolData as School

dataFile = sqlite3.connect("BostixData/Data/USRdata.db") # - Файл базы данных

dataBase = dataFile.cursor()

dataBase.execute('''CREATE TABLE IF NOT EXISTS usersData
            	(userID INTEGER PRIMARY KEY, realName TEXT, birthDate INTEGER, schoolID TEXT)''') # - База данных персональной информации пользователей

dataFile.commit()

dataFile.close()

# - Добавление нового пользователя

def AddNewUser(userID, RealName, SchoolID=0):
    dataFile = sqlite3.connect("BostixData/Data/USRdata.db")

    dataBase = dataFile.cursor()

    dataBase.execute('INSERT INTO usersData (userID, realName, birthDate, schoolID) VALUES (?, ?, ?, ?)', (userID, RealName, 0, SchoolID))

    dataFile.commit()

    dataFile.close()

# - Получение информации о пользователе по ID

def getUserData(userID):
    dataFile = sqlite3.connect("BostixData/Data/USRdata.db")

    dataBase = dataFile.cursor()

    dataBase.execute("SELECT realName, birthDate, schoolID FROM usersData WHERE userID == ?", (userID,))
    return dataBase.fetchone()

# - Изменение статуса заявки на вступление в школу у пользователя

def editSchoolID(userID):
    dataFile = sqlite3.connect("BostixData/Data/USRdata.db")

    dataBase = dataFile.cursor()

    schoolID = "None"

    if len(getUserData(userID)[2].split("-")) > 1:
        if getUserData(userID)[2].split("-")[0] == "Accepted":
            schoolID = getUserData(userID)[2].split("-")[1]
        elif getUserData(userID)[2].split("-")[0] == "Rejected":
            schoolID = "None"

    dataBase.execute("UPDATE usersData SET schoolID = ? WHERE userID = ?", (schoolID, userID))

    dataFile.commit()

    dataFile.close()

# - Обработка запроса на вступление в школу

def replyRequestStatus(userID, requestReply):
    dataFile = sqlite3.connect("BostixData/Data/USRdata.db")

    dataBase = dataFile.cursor()

    if requestReply == "Accept":
        schoolID = f'Accept-{getUserData(userID)[2].split("-")[1]}'
        
        if getUserData(userID)[2].split("-")[0] == "PendingRequest":
            role = "Student"
        elif getUserData(userID)[2].split("-")[0] == "PendingTeacherRequest":
            role = "Teacher"

        School.AddNewMemberToSchool(userID, getUserData(userID)[2].split("-")[1], role)
    elif requestReply == "Reject":
        schoolID = f'Reject-{getUserData(userID)[2].split("-")[1]}'

    dataBase.execute("UPDATE usersData SET schoolID = ? WHERE userID = ?", (schoolID, userID))

    dataFile.commit()

    dataFile.close()

# - Получение данных о заявках в определенную школу

def getUserRequests(schoolLogin):
    dataFile = sqlite3.connect("BostixData/Data/USRdata.db")

    dataBase = dataFile.cursor()

    dataBase.execute("SELECT userID FROM usersData WHERE schoolID == ? OR schoolID == ?", (f'PendingRequest-{schoolLogin}', f'PendingTeacherRequest-{schoolLogin}'))
    return dataBase.fetchall()
