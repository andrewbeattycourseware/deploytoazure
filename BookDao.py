import mysql.connector
from mysql.connector import cursor

import dbconfig as cfg
class BookDao:
    db=""
    def connectToDB(self):
        self.db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['database']
        )
    def __init__(self): 
        self.connectToDB()
    

        #print ("connection made")

    def create(self, book):
        cursor = self.db.cursor()
        sql = "insert into book (ISBN, title, author, price) values (%s,%s,%s,%s)"
        values = [
            book['ISBN'],
            book['title'],
            book['author'],
            book['price']
        ]
        cursor.execute(sql, values)
        self.db.commit()
        return cursor.lastrowid

    def getAll(self):
        cursor = self.db.cursor()
        sql = 'select * from book'
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            resultAsDict = self.convertToDict(result)
            returnArray.append(resultAsDict)

        return returnArray

    # this is a bad function becuase it allows SQL injection
    def searchbytitle(self, title):
        cursor = self.db.cursor()
        # bad bad code DO NOT DO THIS
        sql = "select * from book where title like '%"+title +"%'"
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            resultAsDict = self.convertToDict(result)
            returnArray.append(resultAsDict)

        return returnArray


    def findById(self, ISBN):
        cursor = self.db.cursor()
        # this is will allow sql injection
        sql = "select * from book where ISBN = %s"
        values = [ ISBN ]
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDict(result)
        

    def update(self, book):
       cursor = self.db.cursor()
       sql = "update book set title = %s, author = %s, price = %s where ISBN = %s"
       values = [
           book['title'],
           book['author'],
           book['price'],
           book['ISBN']

       ]
       cursor.execute(sql, values)
       self.db.commit()
       return book

    def delete(self, ISBN):
       cursor = self.db.cursor()
       sql = 'delete from book where ISBN = %s'
       values = [ISBN]
       cursor.execute(sql, values)
       
       return {}



    def convertToDict(self, result):
        colnames = ['ISBN','title', 'author', 'price']
        book = {}

        if result:
            for i , colName in enumerate(colnames):
                value = result[i]
                book[colName] = value
        return book

bookDao = BookDao()
