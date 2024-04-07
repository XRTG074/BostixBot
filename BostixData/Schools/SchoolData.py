import sqlite3 # - Библиотека базы данных

#import BostixData.Users.UsersData as Users

# - Добавление новой школы

def AddNewSchool(schoolLogin):
    dataFile = sqlite3.connect(f"BostixData/Data/Schools/school_{schoolLogin}.db") # - Файл базы данных

    dataBase = dataFile.cursor()

    dataBase.execute('''CREATE TABLE IF NOT EXISTS schoolMembersData
            	    (userID INTEGER PRIMARY KEY, role TEXT, customRole TEXT, gradeName TEXT)''') # - База данных участников школы

    dataFile.commit()

    dataFile.close()

# - Добавление нового класса

def AddNewGrade(schoolLogin, gradeName, headTeacherID, gradeLevel):

    dataFile = sqlite3.connect(f"BostixData/Data/Schools/school_{schoolLogin}.db") # - Файл базы данных

    dataBase = dataFile.cursor()

    dataBase.execute(f'''CREATE TABLE IF NOT EXISTS schoolGradesData
            	    (gradeName TEXT PRIMARY KEY, headTeacherID INTEGER, gradeLevel INTEGER)''') # - База данных классов школы
    
    dataBase.execute(f'INSERT INTO schoolGradesData (gradeName, headTeacherID, gradeLevel) VALUES (?, ?, ?)', (gradeName, headTeacherID, gradeLevel))
    
    dataFile.commit()

    dataFile.close()

    dataFile = sqlite3.connect(f"BostixData/Data/Schools/school_{schoolLogin}.db") # - Файл базы данных

    dataBase = dataFile.cursor()

    dataBase.execute(f'''CREATE TABLE IF NOT EXISTS {gradeName}_gradeMembersData
            	    (userID INTEGER PRIMARY KEY, role TEXT, customRole TEXT)''') # - База данных участников классов школы
    
    dataFile.commit()

    dataFile.close()

    AddNewMemberToGrade(schoolLogin, gradeName, headTeacherID, "Teacher", "Классный руководитель")

# - Добавление нового участника в класс

def AddNewMemberToGrade(schoolLogin, gradeName, userID, role, customRole="None"):
    dataFile = sqlite3.connect(f"BostixData/Data/Schools/school_{schoolLogin}.db") # - Файл базы данных

    dataBase = dataFile.cursor()

    dataBase.execute(f'INSERT INTO {gradeName}_gradeMembersData (userID, role, customRole) VALUES (?, ?, ?)', (userID, role, customRole))

    dataFile.commit()

    dataFile.close()

# - Добавление нового участника в школу

def AddNewMemberToSchool(userID, schoolLogin, role, customRole="None", gradeName="None"):
    dataFile = sqlite3.connect(f"BostixData/Data/Schools/school_{schoolLogin}.db") # - Файл базы данных

    dataBase = dataFile.cursor()

    dataBase.execute('INSERT INTO schoolMembersData (userID, role, customRole, gradeName) VALUES (?, ?, ?, ?)', (userID, role, customRole, gradeName))

    dataFile.commit()

    dataFile.close()

# - Получение информации о пользователе по ID

def getUserData(schoolLogin, userID):
    dataFile = sqlite3.connect(f"BostixData/Data/Schools/school_{schoolLogin}.db") # - Файл базы данных

    dataBase = dataFile.cursor()

    dataBase.execute(f"SELECT role, customRole, gradeName FROM schoolMembersData WHERE userID == ?", (userID,))
    return dataBase.fetchone()

# - Получение всех классов

def getAllGrades(schoolLogin):
    dataFile = sqlite3.connect(f"BostixData/Data/Schools/school_{schoolLogin}.db") # - Файл базы данных

    dataBase = dataFile.cursor()

    try:
        dataBase.execute(f'SELECT * FROM schoolGradesData')
        return dataBase.fetchall()
    except:
        return None