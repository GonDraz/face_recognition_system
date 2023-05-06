import json
import os
from tkinter import *
import mysql.connector

from store.path import Path


class StudentModel:
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

        conn = mysql.connector.connect(
            host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")

        my_cursor = conn.cursor()
        my_cursor.execute(sqlVal, val),
        conn.commit()
        conn.close()

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
