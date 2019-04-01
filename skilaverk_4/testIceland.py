from iceconnect import *

courses = CourseDB()

valm=""
while valm !="6":
    print("\n--------------")
    print("1. CourseDB")
    print("2. ")
    print("3. ")
    print("4. ")
    print("5. ")
    print("6. Hætta")
    print("--------------")
    valm=input("")
    try:
        valm1 = ""
        valm2 = ""
        valm3 = ""
        valm4 = ""
        valm5 = ""
        if valm == "1":
            while valm1 != "5":
                print("\n--------------")
                print("1. Create")
                print("2. Read")
                print("3. Update")
                print("4. Delete")
                print("5. Hætta")
                print("--------------")
                valm1 = input("")
                try:
                    if valm1 == "1":
                        cnumb = input("Course Number: ")
                        cname = input("Course Name: ")
                        ccreds = int(input("Course Credits: "))
                        try:
                            courses.add_course(cnumb, cname, ccreds)
                            print(cnumb, "added")
                        except:
                            pass
                    elif valm1 == "2":
                        cnumb = input("Course Number: ")
                        try:
                            course_info = courses.get_course(cnumb)
                            print("--------------")
                            print("Course Number:", course_info[0], "\nCourse Name:", course_info[1], "\nCourse Credits:", course_info[2])
                        except:
                            pass

                    elif valm1 == "3":
                        cnumb = input("Course Number: ")
                        cname = input("Course Name: ")
                        ccreds = int(input("Course Credits: "))
                        try:
                            courses.update_course(cnumb, cname, ccreds)
                            print(cnumb, "updated")
                        except:
                            pass

                    elif valm1 == "4":
                        cnumb = input("Course Number: ")

                        try:
                            courses.delete_course(cnumb)
                            print(cnumb, "deleted")
                        except:
                            pass








                except:
                    pass

    except:
        pass

'''
valm=""
while valm !="4":
    print("\n--------------")
    print("1. Cities")
    print("2. Hotels")
    print("3. Restaurants")
    print("4. Quit")
    print("--------------")
    valm=input("")
    try:
        valm1 = ""
        valm2 = ""
        valm3 = ""
        if valm == "1":
            while valm1 != "3":
                print("\n--------------")
                print("1. Show Specific")
                print("2. Show All")
                print("3. Quit")
                print("--------------")
                valm1 = input("")
                try:
                    if valm1 == "1":
                        name = input("Name: ").lower()
                        placelist = places.get_place_list()
                        for p in placelist:
                            if p[0].lower() == name:
                                print('Name:', p[0])
                                print('Region:', p[1])
                                print('Website:', p[2])
                    elif valm1 == "2":
                        placelist = places.get_place_list()
                        for p in placelist:
                            print(*p)
                    elif valm1 == "3":
                        print('Exiting Menu')
                except:
                    pass

        elif valm == "2":
            while valm2 != "4":
                print("\n--------------")
                print("1. Find by Hotel name")
                print("2. Find by City name")
                print("3. Find by District name")
                print("4. Quit")
                print("--------------")
                valm2 = input("")
                try:
                    if valm2 == "1":
                        name = input("Hotel name: ").lower()
                        hotelList = hotels.get_hotel_list()
                        for p in hotelList:
                            if p[0].lower() == name:
                                print('Name:', p[0])
                                print('Street Address:', p[1])
                                print('District ID:', p[2])
                                print('City:', p[3])
                                print('Website:', p[4])
                    elif valm2 == "2":
                        name = input("City name: ")
                        hotelbycity = hotels.get_hotel_by_city(name)
                        for x in hotelbycity:
                            print('----------------')
                            print('Name:', x[0])
                            print('Street Address:', x[1])
                            print('City:', x[2])
                            print('Website:', x[3])

                    elif valm2 == "3":
                        name = input("District name: ")
                        hotelbydisctrict = hotels.get_hotel_by_district(name)
                        for x in hotelbydisctrict:
                            print('----------------')
                            print('Name:', x[0])
                            print('Street Address:', x[1])
                            print('City:', x[2])
                            print('Website:', x[3])

                    elif valm2 == "4":
                        print('Exiting Menu')
                except:
                    pass
        elif valm == "3":
            while valm3 != "4":
                print("\n--------------")
                print("1. Show all")
                print("2. Find by City name")
                print("3. Find by District name")
                print("4. Quit")
                print("--------------")
                valm3 = input("")
                try:
                    if valm3 == "1":
                        restaurantlist = restaurants.get_restaurant_list()
                        for p in restaurantlist:
                            print(*p)
                    elif valm3 == "2":
                        name = input("City name: ")
                        restaurantbycity = restaurants.get_restaurant_by_city(name)
                        for x in restaurantbycity:
                            print('----------------')
                            print('Name:', x[0])
                            print('Street Address:', x[1])
                            print('City Name:', x[2])
                            print('Capacity:', x[3])
                            print('Website:', x[4])
                    elif valm3 == "3":
                        name = input("District name: ")
                        restaurantbydistrict = restaurants.get_restaurant_by_district(name)
                        for x in restaurantbydistrict:
                            print('----------------')
                            print('Name:', x[0])
                            print('Street Address:', x[1])
                            print('City Name:', x[2])
                            print('Capacity:', x[3])
                            print('Website:', x[4])
                    elif valm3 == "4":
                        print('Exiting Menu')

                except:
                    pass

        elif valm == "4":
            print("Exiting program")

    except:
        pass

'''
