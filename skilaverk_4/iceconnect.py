from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import json

class DbConnector:
    def __init__(self):
        self.db_config = read_db_config()
        self.status = ' '
        try:
            self.conn = MySQLConnection(**self.db_config)
            if self.conn.is_connected():
                self.status = 'OK'
            else:
                self.status = 'connection failed.'
        except Error as error:
            self.status = error

    def execute_function(self, func_header=None, argument_list=None):
        cursor = self.conn.cursor()
        try:
            if argument_list:
                func = func_header % argument_list
            else:
                func = func_header
            cursor.execute(func)
            result = cursor.fetchone()
        except Error as e:
            self.status = e
            result = None
        finally:
            cursor.close()
        return result[0]

    def execute_procedure(self, proc_name, argument_list=None):
        result_list = list()
        cursor = self.conn.cursor()
        try:
            if argument_list:
                cursor.callproc(proc_name, argument_list)
            else:
                cursor.callproc(proc_name)
            self.conn.commit()
            for result in cursor.stored_results():
                result_list = [list(elem) for elem in result.fetchall()]
        except Error as e:
            self.status = e
        finally:
            cursor.close()
        return result_list


class CourseDB(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_course(self, c_numb, c_name, c_cred):
        new_id = 0
        result = self.execute_procedure('NewCourse', [c_numb, c_name, c_cred])
        if result:
            new_id = int(result[0][0])
        return new_id

    def get_course(self, c_numb):
        result = self.execute_procedure('SingleCourse', [c_numb])
        if result:
            return result[0]
        else:
            return list()

    def get_restrictors(self):
        result = self.execute_procedure('courseRestrictorList')
        if result:
            return result
        else:
            return list()

    def number_of_courses(self):
        result = self.execute_function('NumberOfCourses')
        if result:
            return result[0]
        else:
            return list()

    def update_course(self, c_numb, c_name, c_cred):
        rows_affected = 0
        result = self.execute_procedure('UpdateCourse', [c_numb, c_name, c_cred])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delete_course(self, c_numb):
        rows_affected = 0
        result = self.execute_procedure('DeleteCourse', [c_numb])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected


class StudentDB(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_student(self, s_fname, s_lname, s_dob, s_ss):
        new_id = 0
        result = self.execute_procedure('AddStudent', [s_fname, s_lname, s_dob, s_ss])
        if result:
            new_id = int(result[0][0])
        return new_id

    def get_student(self, s_id):
        result = self.execute_procedure('SingleStudentJSON', [s_id])
        if result:
            return result[0]
        else:
            return list()

    def student_creds(self, s_id):
        result = self.execute_procedure('studentCreds', [s_id])
        if result:
            return result[0]
        else:
            return list()

    def update_student(self, s_id, s_ss):
        rows_affected = 0
        result = self.execute_procedure('UpdateStudent', [s_id, s_ss])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delete_student(self, s_id):
        rows_affected = 0
        result = self.execute_procedure('DeleteStudent', [s_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

class SchoolDB(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_school(self, school_name):
        new_id = 0
        result = self.execute_procedure('AddSchool', [school_name])
        if result:
            new_id = int(result[0][0])
        return new_id

    def get_school(self, school_id):
        result = self.execute_procedure('SingleSchool', [school_id])
        if result:
            return result[0]
        else:
            return list()

    def update_school(self, school_id, s_name):
        rows_affected = 0
        result = self.execute_procedure('UpdateSchool', [school_id, s_name])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delete_school(self, school_id):
        rows_affected = 0
        result = self.execute_procedure('DeleteSchool', [school_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected
