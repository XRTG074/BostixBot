import sqlite3 # - Библиотека базы данных

dataFile = sqlite3.connect("BostixData/Data/UPdata.db") # - Файл базы данных

dataBase = dataFile.cursor()

dataBase.execute('''CREATE TABLE IF NOT EXISTS usersPersonalData
            	(userID INTEGER PRIMARY KEY, realName TEXT, birthDate INTEGER, schoolID INTEGER)''') # - База данных персональной информации пользователей

dataFile.commit()

dataFile.close()

# - Добавление нового пользователя

def AddNewUser(UserID, RealName, SchoolID=0):
    dataFile = sqlite3.connect("BostixData/Data/UPdata.db")

    dataBase = dataFile.cursor()

    dataBase.execute('INSERT INTO usersPersonalData (userID, realName, birthDate, schoolID) VALUES (?, ?, ?, ?)', (UserID, RealName, 0, SchoolID))

    dataFile.commit()

    dataFile.close()

# - Получение информации о пользователе по ID

def getUserData(UserID):
    dataFile = sqlite3.connect("BostixData/Data/UPdata.db")

    dataBase = dataFile.cursor()

    dataBase.execute("SELECT realName, birthDate, schoolID FROM usersPersonalData WHERE userID == ?", (UserID,))
    return dataBase.fetchone()