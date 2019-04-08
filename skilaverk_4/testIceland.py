from iceconnect import *

courses = CourseDB()
students = StudentDB()
schools = SchoolDB()

valm=""
while valm !="6":
    print("\n--------------")
    print("1. CourseDB")
    print("2. StudentDB")
    print("3. SchoolDB")
    print("4. ")
    print("5. ")
    print("6. Hætta")
    print("--------------")
    valm=input("")
    try:
        courseValm = ""
        studentValm = ""
        schoolValm = ""
        valm4 = ""
        valm5 = ""
        if valm == "1":
            while courseValm != "7":
                print("\n--------------")
                print("1. New Course")
                print("2. Course Info")
                print("3. Course Restrictors")
                print("4. Number Of Courses")
                print("5. Update Course")
                print("6. Delete Course")
                print("7. Hætta")
                print("--------------")
                courseValm = input("")
                try:
                    if courseValm == "1":
                        cnumb = input("Course Number: ")
                        cname = input("Course Name: ")
                        ccreds = int(input("Course Credits: "))
                        try:
                            courses.add_course(cnumb, cname, ccreds)
                            print(cnumb, "added")
                        except:
                            pass
                    elif courseValm == "2":
                        cnumb = input("Course Number: ")
                        try:
                            course_info = courses.get_course(cnumb)
                            print("--------------")
                            print("Course Number:", course_info[0], "\nCourse Name:", course_info[1], "\nCourse Credits:", course_info[2])
                        except:
                            pass

                    elif courseValm == "3":
                        try:
                            restrictor_info = courses.get_restrictors()
                            print("Course Number\tCourse Name\tCredits\tRestrictor\tRestrictorType")
                            print("---------------------------------------------------------------------------")
                            for restr in restrictor_info:
                                print(restr[0], "\t", restr[1], "\t", restr[2], "\t", restr[4], "\t", restr[5])
                        except:
                            pass

                    elif courseValm == "4":
                        totalCourses = courses.number_of_courses()
                        try:
                            print("Total Number Of Courses:", totalCourses)
                        except:
                            pass

                    elif courseValm == "5":
                        cnumb = input("Course Number: ")
                        cname = input("Course Name: ")
                        ccreds = int(input("Course Credits: "))
                        try:
                            courses.update_course(cnumb, cname, ccreds)
                            print(cnumb, "updated")
                        except:
                            pass

                    elif courseValm == "6":
                        cnumb = input("Course Number: ")

                        try:
                            courses.delete_course(cnumb)
                            print(cnumb, "deleted")
                        except:
                            pass
                except:
                    pass

        elif valm == "2":
            while studentValm != "6":
                print("\n--------------")
                print("1. New Student")
                print("2. Student Info")
                print("3. Student Credits")
                print("4. Update Student")
                print("5. Delete Student")
                print("6. Hætta")
                print("--------------")
                studentValm = input("")
                try:
                    if studentValm == "1":
                        fName = input("First Name: ")
                        lName = input("Last Name: ")
                        dob = int(input("Date of Birth: "))
                        startSem = int(input("Starting Semester: "))

                        try:
                            students.add_student(fName, lName, dob, startSem)
                            print(fName, "", lName, "added")
                        except:
                            pass
                    elif studentValm == "2":
                        studentId = int(input("Student ID: "))

                        student = students.get_student(studentId)
                        parsed = json.loads(student[0])

                        try:
                            print("Student ID: ", parsed["s_id"])
                            print("First Name: ", parsed["f_name"])
                            print("Last Name: ", parsed["l_name"])
                            print("Date of Birth: ", parsed["date_of_b"])
                            print("Courses: ")
                            for courses in json.loads(parsed["course_list"]):
                                print("Course Number: ", courses["c_number"])
                                print("Course Credits: ", courses["c_credits"])
                                print("Course Status: ", courses["course_status"])
                        except:
                            pass

                    elif studentValm == "3":
                        studentId = int(input("Student ID: "))
                        student = students.student_creds(studentId)

                        try:
                            print("Student Name:", student[0], "\nNams Braut:", student[1], "\nFjoldi Einigar:", student[2])

                        except:
                            pass

                    elif studentValm == "4":
                        studentId = int(input("Student ID: "))
                        ss = int(input("Starting Semester: "))
                        try:
                            students.update_student(studentId, ss)
                            print(studentId, "'s starting semester updated")
                        except:
                            pass

                    elif studentValm == "5":
                        studentId = int(input("Student ID: "))

                        try:
                            students.delete_student(studentId)
                            print(studentId, "deleted")
                        except:
                            pass
                except:
                    pass

        elif valm == "3":
            while schoolValm != "5":
                print("\n--------------")
                print("1. New School")
                print("2. School Info")
                print("3. Update School")
                print("4. Delete School")
                print("5. Hætta")
                print("--------------")
                schoolValm = input("")
                try:
                    if schoolValm == "1":
                        schoolName = input("School Name: ")

                        try:
                            schools.add_school(schoolName)
                            print(schoolName, "added")
                        except:
                            pass
                    elif schoolValm == "2":
                        schoolId = int(input("School ID: "))

                        try:
                            schoolInfo = schools.get_school(schoolId)
                            print("--------------")
                            print("School ID:", schoolInfo[0], "\nSchool Name:", schoolInfo[1])
                        except:
                            pass

                    elif schoolValm == "3":
                        schoolId = int(input("School ID: "))
                        schoolName = input("School Name: ")
                        try:
                            schools.update_school(schoolId, schoolName)
                            print(schoolId, "updated")
                        except:
                            pass

                    elif schoolValm == "4":
                        schoolId = int(input("School ID: "))

                        try:
                            schools.delete_school(schoolId)
                            print(schoolId, "deleted")
                        except:
                            pass

                except:
                    pass
    except:
        pass
