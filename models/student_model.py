import json
import os
import shutil
from tkinter import *
import mysql.connector
from store.my_sql_setting import MySqlSetting

from store.path import Path


class StudentModel:
    conn = mysql.connector.connect(
        host=MySqlSetting.host, username=MySqlSetting.username, password=MySqlSetting.password, database=MySqlSetting.database)

    my_cursor = conn.cursor()

    # def __init__(self):
    #     pass

    def addStudent(self, var_dep, var_course, var_year, var_semester, var_std_id, var_std_name, var_div, var_roll, var_gender, var_dob, var_mail, var_phone, var_address, var_teacher, var_radio1):
        sqlCmt = "INSERT INTO student "
        sqlColumn = sqlCmt + \
            "(dep,course,year,semester,studentID,name,division,Roll,gender,Dob,mail,phone,Address,teacher,photoSample) "
        sqlVal = sqlColumn + \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (var_dep, var_course, var_year, var_semester, var_std_id, var_std_name, var_div,
               var_roll, var_gender, var_dob, var_mail, var_phone, var_address, var_teacher, var_radio1)

        self.my_cursor.execute(sqlVal, val),
        self.conn.commit()

        path = Path.Data.images
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, f"{var_std_id}")
        os.makedirs(path, exist_ok=True)
        path = Path.Data.info
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, f"{var_std_id}.json")

        studentData = {
            "dep": var_dep,
            "course": var_course,
            "year": var_year,
            "semester": var_semester,
            "id": var_std_id,
            "name": var_std_name,
            "div": var_div,
            "roll": var_roll,
            "gender": var_gender,
            "dob": var_dob,
            "mail": var_mail,
            "phone": var_phone,
            "address": var_address,
            "teacher": var_teacher,
        }
        with open(path, "w", encoding='utf-8') as outfile:
            json.dump(studentData, outfile, ensure_ascii=False)
        return

    def LoadStudent(self):

        self.my_cursor.execute("select * from student")
        data = self.my_cursor.fetchall()
        self.conn.commit()
        return data

    def updateStudent(self, var_dep, var_course, var_year, var_semester, var_std_id, var_std_name, var_div, var_roll, var_gender, var_dob, var_mail, var_phone, var_address, var_teacher, var_radio1):
        sqlCmt = "update student set "
        sqlColumn = sqlCmt + \
            "dep=%s,course=%s,year=%s,semester=%s,name=%s,division=%s,Roll=%s,gender=%s,Dob=%s,mail=%s,phone=%s,Address=%s,teacher=%s,photoSample=%s where studentID=%s"
        sqlVal = sqlColumn
        val = (var_dep, var_course, var_year, var_semester, var_std_name, var_div,
               var_roll, var_gender, var_dob, var_mail, var_phone, var_address, var_teacher, var_radio1, var_std_id)

        self.my_cursor.execute(sqlVal, val),
        self.conn.commit()

        n = str(var_std_id)
        path = Path.Data.info
        path = os.path.join(path, n + ".json")

        studentData = {
            "dep": var_dep,
            "course": var_course,
            "year": var_year,
            "semester": var_semester,
            "id": var_std_id,
            "name": var_std_name,
            "div": var_div,
            "roll": var_roll,
            "gender": var_gender,
            "dob": var_dob,
            "mail": var_mail,
            "phone": var_phone,
            "address": var_address,
            "teacher": var_teacher,
        }
        with open(path, "w", encoding='utf-8') as outfile:
            json.dump(studentData, outfile, ensure_ascii=False)

    def deleteStudent(self, var_std_id):
        sql = "delete from student where studentID=%s"
        val = (var_std_id,)
        self.my_cursor.execute(sql, val)

        self.conn.commit()

        n = str(var_std_id)
        path = Path.Data.images + n
        shutil.rmtree(path)
        path = Path.Data.info + n + ".json"
        os.remove(path)

    def deleteAll(self):
        sql = "delete from student"
        self.my_cursor.execute(sql)
        self.conn.commit()
        if os.path.exists("data"):
            shutil.rmtree("data")
        if os.path.exists("attendance"):
            shutil.rmtree("attendance")
