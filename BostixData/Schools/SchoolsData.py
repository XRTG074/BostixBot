import sqlite3 # - Библиотека базы данных

import random

dataFile = sqlite3.connect("BostixData/Data/SCHdata.db") # - Файл базы данных

dataBase = dataFile.cursor()

dataBase.execute('''CREATE TABLE IF NOT EXISTS schoolsData
            	(schoolLogin TEXT PRIMARY KEY, schoolID INTEGER, schoolName TEXT)''') # - База данных школ

dataFile.commit()

dataFile.close()

# - Добавление новой школы

def AddNewSchool(schoolLogin, schoolName):

    # - Генерация уникального ID для школы

    while True:
        schoolID = random.randint(15000000000, 99999999999)
        if checkIDUniqueness(schoolID) is None:
            break

    dataFile = sqlite3.connect("BostixData/Data/SCHdata.db")

    dataBase = dataFile.cursor()
    dataBase.execute('INSERT INTO schoolsData (schoolLogin, schoolID, schoolName) VALUES (?, ?, ?)', (str(schoolLogin), schoolID, str(schoolName)))

    dataFile.commit()

    dataFile.close()

# - Получение информации о школе

def getSchoolData(schoolLogin):
    dataFile = sqlite3.connect("BostixData/Data/SCHdata.db")

    dataBase = dataFile.cursor()

    dataBase.execute("SELECT schoolID, schoolName FROM schoolsData WHERE schoolLogin == ?", (str(schoolLogin),))
    return dataBase.fetchone()

# - Проверка сгенерированного ID на уникальность

def checkIDUniqueness(ID):
    dataFile = sqlite3.connect("BostixData/Data/SCHdata.db")

    dataBase = dataFile.cursor()

    dataBase.execute("SELECT schoolName FROM schoolsData WHERE schoolID == ?", (ID,))

    return dataBase.fetchone()