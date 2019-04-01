from tkinter import *
import os
from iceconnect import *

places = PlaceDB()
hotels = HotelDB()
restaurants = RestaurantDB()
loginProc = UserDB()

def Login():
    global nameEL
    global pwordEL  # More globals :D
    global rootA

    rootA = Tk()  # This now makes a new window.
    rootA.title('Login')  # This makes the window title 'login'

    intruction = Label(rootA, text='Please Login\n')  # More labels to tell us what they do
    intruction.grid(sticky=E)  # Blahdy Blah

    nameL = Label(rootA, text='Username: ')  # More labels
    pwordL = Label(rootA, text='Password: ')  # ^
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)

    nameEL = Entry(rootA)  # The entry input
    pwordEL = Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)

    loginB = Button(rootA, text='Login',
                    command=CheckLogin)  # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(columnspan=2, sticky=W)


    rootA.mainloop()


def CheckLogin():
    loginAttempt = loginProc.login(nameEL.get(), pwordEL.get())
    for logdetails in loginAttempt:
        uname = logdetails[0]
        pword = logdetails[1]
        adminPriv = logdetails[2]
        if nameEL.get() == uname and pwordEL.get() == pword and adminPriv == 'False':  # Checks to see if you entered the correct data.
            rootA.destroy() #slekkur a login
            Vidmot() #kveikur a vidmotinu
        elif nameEL.get() == uname and pwordEL.get() == pword and adminPriv == 'True':
            rootA.destroy()
            adminVidmot()
        else:
            r = Tk()
            r.title('D:')
            r.geometry('150x50')
            rlbl = Label(r, text='\n[!] Invalid Login')
            rlbl.pack()
            r.mainloop()



def Vidmot():

    rootB = Tk()
    rootB.title("Main Menu")

    citiesB = Button(rootB, text="Find cities", command=citiesMenu)
    citiesB.grid(columnspan=2)
    hotelsB = Button(rootB, text="Find hotels", command=hotelsMenu)
    hotelsB.grid(columnspan=2)
    restaurantsB = Button(rootB, text="Find restaurants", command=restaurantsMenu)
    restaurantsB.grid(columnspan=2)

    rootB.mainloop()


def adminVidmot():
    aRootB = Tk()
    aRootB.title("Admin Menu")

    placesB = Button(aRootB, text="Manage PlaceDB", command=managePlaces)
    placesB.grid(columnspan=2)
    hotelsB = Button(aRootB, text="Manage HotelDB")
    hotelsB.grid(columnspan=2)
    #restaurantsB = Button(rootB, text="Find restaurants", command=restaurantsMenu)
    #restaurantsB.grid(columnspan=2)

    aRootB.mainloop()

def managePlaces():
    aRootPlaces = Tk()
    aRootPlaces.title("Manage Places")

    aRootPlaces.geometry('100x70')

    var = StringVar(aRootPlaces)
    var.set("Create")

    option = OptionMenu(aRootPlaces, var, "Create", "Read", "Update", "Delete", "Quit")
    option.pack()

    def placesCRUD():

        def PlacesCreate():
            if len(placeNameEL.get()) > 0 and len(placeRegionEL.get()) > 0 and len(placePopEL.get()) > 0 and len(placeWebsEL.get()) > 0 and len(placeLatEL.get()) > 0 and len(placeLongEL.get()) > 0:
                try:
                    places.add_place(placeNameEL.get(), placeRegionEL.get(), placePopEL.get(), placeWebsEL.get(), placeLatEL.get(), placeLongEL.get())
                    createPlaces.destroy()
                    createSuc = Tk()
                    createSuc.title('Create Success')
                    createSuc.geometry('150x50')
                    createSuclbl = Label(createSuc, text='\n[!] Submit successful')
                    createSuclbl.pack()
                    createSuc.mainloop()
                except:
                    pass
            else:
                createEr = Tk()
                createEr.title('Create Error')
                createEr.geometry('150x50')
                createErlbl = Label(createEr, text='\n[!] Submit failed')
                createErlbl.pack()
                createEr.mainloop()

        def PlacesUpdate():

            def PlacesUpdateFinal():
                # try:

                print(placeIdE.get(), uPlaceNameEL.get(), uPlaceRegionEL.get(), uPlacePopEL.get(), uPlaceWebsEL.get())
                places.update_place(placeIdE.get(), uPlaceNameEL.get(), uPlaceRegionEL.get(), uPlacePopEL.get(), uPlaceWebsEL.get())
                # except:
                #    pass

            placeNameTempL = []
            placeRegionTempL = []
            placeWebTempL = []
            placePopTempL = []
            placelist = places.get_place_list()
            for pl in placelist:
                if str(pl[4]) == placeIdE.get():
                    #specifyPlace.destroy()
                    placeNameTemp = pl[0] + ""
                    placeRegionTemp = pl[1] + ""
                    placeWebTemp = str(pl[2]) + ""
                    placePopTemp = str(pl[3]) + ""
                    placeNameTempL.append(placeNameTemp)
                    placeRegionTempL.append(placeRegionTemp)
                    placeWebTempL.append(placeWebTemp)
                    placePopTempL.append(placePopTemp)

            updatePlaces = Tk()
            updatePlaces.title('Update Place')
            updatePlaces.geometry('200x160')

            uPlaceNameL = Label(updatePlaces, text='Name: ')
            uPlaceRegionL = Label(updatePlaces, text='Region: ')
            uPlaceWebsL = Label(updatePlaces, text='Website: ')
            uPlacePopL = Label(updatePlaces, text='Population: ')

            uPlaceNameL.grid(row=1, sticky=W)
            uPlaceRegionL.grid(row=2, sticky=W)
            uPlaceWebsL.grid(row=3, sticky=W)
            uPlacePopL.grid(row=4, sticky=W)

            uPlaceNameEL = Entry(updatePlaces)
            uPlaceNameEL.insert(0, placeNameTempL[0])
            uPlaceRegionEL = Entry(updatePlaces)
            uPlaceRegionEL.insert(0, placeRegionTempL[0])
            uPlaceWebsEL = Entry(updatePlaces)
            uPlaceWebsEL.insert(0, placeWebTempL[0])
            uPlacePopEL = Entry(updatePlaces)
            uPlacePopEL.insert(0, placePopTempL[0])

            uPlaceNameEL.grid(row=1, column=1)
            uPlaceRegionEL.grid(row=2, column=1)
            uPlaceWebsEL.grid(row=3, column=1)
            uPlacePopEL.grid(row=4, column=1)

            print(placeIdE.get(), uPlaceNameEL.get(), uPlaceRegionEL.get(), uPlacePopEL.get(), uPlaceWebsEL.get())

            submitB = Button(updatePlaces, text='Submit', command=PlacesUpdateFinal)
            submitB.grid(columnspan=2, sticky=W)

            updatePlaces.mainloop()


        if str(var.get()) == 'Create':
            try:
                createPlaces = Tk()
                createPlaces.title('Add New Place')
                createPlaces.geometry('200x160')

                placeNameL = Label(createPlaces, text='Name: ')
                placeRegionL = Label(createPlaces, text='Region: ')
                placePopL = Label(createPlaces, text='Population: ')
                placeWebsL = Label(createPlaces, text='Website: ')
                placeLatL = Label(createPlaces, text='Latitude: ')
                placeLongL = Label(createPlaces, text='Longitude: ')

                placeNameL.grid(row=1, sticky=W)
                placeRegionL.grid(row=2, sticky=W)
                placePopL.grid(row=3, sticky=W)
                placeWebsL.grid(row=4, sticky=W)
                placeLatL.grid(row=5, sticky=W)
                placeLongL.grid(row=6, sticky=W)

                placeNameEL = Entry(createPlaces)
                placeRegionEL = Entry(createPlaces)
                placePopEL = Entry(createPlaces)
                placeWebsEL = Entry(createPlaces)
                placeLatEL = Entry(createPlaces)
                placeLongEL = Entry(createPlaces)

                placeNameEL.grid(row=1, column=1)
                placeRegionEL.grid(row=2, column=1)
                placePopEL.grid(row=3, column=1)
                placeWebsEL.grid(row=4, column=1)
                placeLatEL.grid(row=5, column=1)
                placeLongEL.grid(row=6, column=1)

                submitB = Button(createPlaces, text='Submit', command=PlacesCreate)
                submitB.grid(columnspan=2, sticky=W)

                createPlaces.mainloop()
            except:
                pass

        elif str(var.get()) == 'Read':
            try:
                allPlaces = Tk()
                allPlaces.title('All the cities')
                allPlaces.geometry('450x200')
                string = '\n'
                tmplist = ["City            Region            Website"]
                placelist = places.get_place_list()
                for p in placelist:
                    test = p[0] + " | " + p[1] + " | " + p[2]
                    tmplist.append(test)

                tmplist2 = [str(x) + string for x in tmplist]
                allPlaceslbl = Label(allPlaces, text=" ".join(tmplist2), justify='left')
                allPlaceslbl.pack()
                allPlaces.mainloop()
            except:
                pass

        elif str(var.get()) == 'Update':
            specifyPlace = Tk()
            specifyPlace.title('Specify Place')

            placeIdL = Label(specifyPlace, text='Place ID: ')
            placeIdL.grid(row=1, sticky=W)
            placeIdE = Entry(specifyPlace)
            placeIdE.grid(row=1, column=1)

            submitB = Button(specifyPlace, text='Submit', command=PlacesUpdate)
            submitB.grid(columnspan=2, sticky=W)

            specifyPlace.mainloop()


        elif str(var.get()) == 'Quit':
            try:
                aRootPlaces.destroy()
            except:
                pass

    button = Button(aRootPlaces, text="OK", command=placesCRUD)
    button.pack()

    aRootPlaces.mainloop()


def citiesMenu():
    rootC = Tk()
    rootC.title("City Menu")
    rootC.geometry('300x300')

    var = StringVar(rootC)
    var.set("Show Specific")

    option = OptionMenu(rootC, var, "Show All", "Show Specific", "Quit")
    option.pack()

    def showPlaces():
        if str(var.get()) == 'Show All':
            allPlaces = Tk()
            allPlaces.title('All the cities')
            allPlaces.geometry('450x200')
            string = '\n'
            tmplist = ["City            Region            Website"]
            placelist = places.get_place_list()
            for p in placelist:
                test = p[0] + " | " + p[1] + " | " + p[2]
                tmplist.append(test)

            tmplist2 = [str(x) + string for x in tmplist]
            allPlaceslbl = Label(allPlaces, text=" ".join(tmplist2), justify='left')
            allPlaceslbl.pack()
            allPlaces.mainloop()

        elif str(var.get()) == 'Show Specific':
            spePlaceSear = Tk()
            spePlaceSear.title('Specific City Search')
            spePlaceSear.geometry('450x200')
            instruction = Label(spePlaceSear, text='Please enter the name\n')
            instruction.grid(sticky=E)

            Cname = Label(spePlaceSear, text='City name: ')
            Cname.grid(row=1, sticky=W)

            CnameE = Entry(spePlaceSear)
            CnameE.grid(row=1, column=1)

            def SearchPlaces():
                specificPlace = Tk()
                specificPlace.title('Specific City')
                specificPlace.geometry('450x200')
                string = '\n'
                tmplist = ["City             Region                 Website"]
                placelist = places.get_place_list()
                for p in placelist:
                    if p[0].lower() == CnameE.get():
                        test = p[0] + " | " + p[1] + " | " + p[2]
                        tmplist.append(test)

                tmplist2 = [str(x) + string for x in tmplist]
                spePlaceLab = Label(specificPlace, text=" ".join(tmplist2), justify='left')
                spePlaceLab.pack()
                specificPlace.mainloop()

            searchB = Button(spePlaceSear, text='Search', command=SearchPlaces)
            searchB.grid(columnspan=2, sticky=W)

            spePlaceSear.mainloop()

        elif str(var.get()) == "Quit":
            try:
                rootC.destroy()
            except:
                pass

    button = Button(rootC, text="OK", command=showPlaces)
    button.pack()

    rootC.mainloop()

def hotelsMenu():
    rootH = Tk()
    rootH.title("Hotel Menu")
    rootH.geometry('200x75')

    var = StringVar(rootH)
    var.set("Find by Hotel name")


    option = OptionMenu(rootH, var, "Find by Hotel name", "Find by City name", "Find by District name", "Quit")
    option.pack()

    def showHotels():
        rootH.destroy()
        if str(var.get()) == 'Find by Hotel name':
            hbhnSearch = Tk() #hotel by hotel name
            hbhnSearch.title('Hotel By Hotel Name Search')
            hbhnSearch.geometry('200x100')

            Hname = Label(hbhnSearch, text='Hotel name: ')
            Hname.grid(row=1, sticky=W)

            HnameE = Entry(hbhnSearch)
            HnameE.grid(row=1, column=1, sticky=W)


            def SearcHotels():
                hotelnameentry = HnameE.get()
                hotelname = ""
                hbhnSearch.destroy()
                hotelNameSearch = Tk()

                hotelNameSearch.geometry('450x200')
                tmplist = []
                namelist = ["Hotel name: "]
                addresslist = ["Street Address: "]
                districtIDlist = ["District ID: "]
                citylist = ["City: "]
                websitelist = ["Website: "]
                hotelList = hotels.get_hotel_list()
                for h in hotelList:
                    if h[0].lower() == hotelnameentry.lower():
                        hotelname += h[0]
                        nametest = h[0] + " "
                        addresstest = h[1] + " "
                        distrtest = str(h[2]) + " "
                        citytest = h[3] + " "
                        webtest = h[4] + " "
                        namelist.append(nametest)
                        addresslist.append(addresstest)
                        districtIDlist.append(distrtest)
                        citylist.append(citytest)
                        websitelist.append(webtest)
                hotelNameSearch.title(hotelname)
                teljari = 0
                for hn in namelist:
                    teljari += 1
                    if teljari == 2:
                        tmplist.append(hn)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != 2:
                        tmplist.append(hn)
                for addstr in addresslist:
                    teljari += 1
                    if teljari == 2:
                        tmplist.append(addstr)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != 2:
                        tmplist.append(addstr)
                for distrid in districtIDlist:
                    teljari += 1
                    if teljari == 2:
                        tmplist.append(distrid)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != 2:
                        tmplist.append(distrid)
                for cn in citylist:
                    teljari += 1
                    if teljari == 2:
                        tmplist.append(cn)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != 2:
                        tmplist.append(cn)
                for wn in websitelist:
                    teljari += 1
                    if teljari == 2:
                        tmplist.append(wn)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != 2:
                        tmplist.append(wn)
                hnsLab = Label(hotelNameSearch, text="".join(tmplist), justify='left')
                hnsLab.pack()
                hotelNameSearch.mainloop()

            searchB = Button(hbhnSearch, text='Search', command=SearcHotels)
            searchB.grid(columnspan=2, sticky=W)

            hbhnSearch.mainloop()

        elif str(var.get()) == 'Find by City name':
            hbcnSearch = Tk()  # hotel by city name
            hbcnSearch.title('Hotel By City Name Search')
            hbcnSearch.geometry('200x100')

            Hname = Label(hbcnSearch, text='City name: ')
            Hname.grid(row=1, sticky=W)

            HnameE = Entry(hbcnSearch)
            HnameE.grid(row=1, column=1, sticky=W)

            def Hotelsbycity():
                citynameentry = HnameE.get()
                hotelname = ""
                hbcnSearch.destroy()
                hotelbycitySearch = Tk()
                hotelbycitySearch.geometry('450x200')
                tmplist = []
                namelist = ["Hotel name: "]
                addresslist = ["Street Address: "]
                districtIDlist = ["District ID: "]
                citylist = ["City: "]
                websitelist = ["Website: "]
                hotelList = hotels.get_hotel_list()
                for h in hotelList:
                    if h[3].lower() == citynameentry.lower():
                        hotelname += h[0]
                        nametest = h[0] + ""
                        addresstest = h[1] + ""
                        distrtest = str(h[2]) + ""
                        citytest = h[3] + ""
                        webtest = h[4] + ""
                        namelist.append(nametest)
                        addresslist.append(addresstest)
                        districtIDlist.append(distrtest)
                        citylist.append(citytest)
                        websitelist.append(webtest)
                hotelbycitySearch.title(hotelname)
                teljari = 0
                for hn in namelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(", ")
                        tmplist.append(hn)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(hn)
                for addstr in addresslist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(", ")
                        tmplist.append(addstr)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(addstr)
                for distrid in districtIDlist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(", ")
                        tmplist.append(distrid)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(distrid)
                for cn in citylist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(", ")
                        tmplist.append(cn)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(cn)
                for wn in websitelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(", ")
                        tmplist.append(wn)
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(wn)
                hnsLab = Label(hotelbycitySearch, text="".join(tmplist), justify='left')
                hnsLab.pack()
                hotelbycitySearch.mainloop()

            searchB = Button(hbcnSearch, text='Search', command=Hotelsbycity)
            searchB.grid(columnspan=2, sticky=W)

            hbcnSearch.mainloop()

        elif str(var.get()) == 'Find by District name':
            hbdnSearch = Tk()  # hotel by district name
            hbdnSearch.title('Hotel By District Name Search')
            hbdnSearch.geometry('200x100')

            Hname = Label(hbdnSearch, text='District name: ')
            Hname.grid(row=1, sticky=W)

            HnameE = Entry(hbdnSearch)
            HnameE.grid(row=1, column=1, sticky=W)

            def Hotelsbydistrict():
                districtnameentry = HnameE.get()
                hotelname = ""
                hbdnSearch.destroy()
                hotelbydistrictSearch = Tk()
                hotelbydistrictSearch.geometry('450x200')
                tmplist = []
                namelist = ["Hotel name: "]
                addresslist = ["Street Address: "]
                citylist = ["City: "]
                websitelist = ["Website: "]
                hotelbydisctrict = hotels.get_hotel_by_district(districtnameentry)
                for h in hotelbydisctrict:
                    hotelname += h[0]
                    nametest = h[0] + ""
                    addresstest = h[1] + ""
                    citytest = h[2] + ""
                    webtest = h[3] + ""
                    namelist.append(nametest)
                    addresslist.append(addresstest)
                    citylist.append(citytest)
                    websitelist.append(webtest)
                hotelbydistrictSearch.title(hotelname)
                teljari = 0
                for hn in namelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(hn)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(hn)
                for addstr in addresslist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(addstr)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(addstr)
                for cn in citylist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(cn)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(cn)
                for wn in websitelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(wn)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(wn)
                hnsLab = Label(hotelbydistrictSearch, text="".join(tmplist), justify='left')
                hnsLab.pack()
                hotelbydistrictSearch.mainloop()

            searchB = Button(hbdnSearch, text='Search', command=Hotelsbydistrict)
            searchB.grid(columnspan=2, sticky=W)

            hbdnSearch.mainloop()

    button = Button(rootH, text="OK", command=showHotels)
    button.pack()

    rootH.mainloop()

def restaurantsMenu():
    rootR = Tk()
    rootR.title("Restaurant Menu")
    rootR.geometry('200x75')

    var = StringVar(rootR)
    var.set("Show All")


    option = OptionMenu(rootR, var, "Show All", "Find by City name", "Find by District name", "Quit")
    option.pack()

    def showRestaurants():
        rootR.destroy()
        if str(var.get()) == 'Show All':
            allRestau = Tk() #hotel by hotel name
            allRestau.title('All Restaurants')
            allRestau.geometry('450x200')
            tmplist = []
            namelist = ["Hotel name: "]
            addresslist = ["Street Address: "]
            distrlist = ["District name: "]
            phonelist = ["Phone Number: "]
            restaurantlist = restaurants.get_restaurant_list()
            for r in restaurantlist:
                restName = r[0] + ""
                straddress = r[1] + ""
                distrName = r[3] + ""
                phonenr = str(r[4]) + ""
                namelist.append(restName)
                addresslist.append(straddress)
                distrlist.append(distrName)
                phonelist.append(phonenr)

            teljari = 0
            for hn in namelist:
                teljari += 1
                if teljari == len(namelist):
                    tmplist.append(hn)
                    tmplist.append(", ")
                    tmplist.append("\n")
                    teljari = 0
                elif teljari != len(namelist):
                    tmplist.append(hn)
            for addstr in addresslist:
                teljari += 1
                if teljari == len(namelist):
                    tmplist.append(addstr)
                    tmplist.append(", ")
                    tmplist.append("\n")
                    teljari = 0
                elif teljari != len(namelist):
                    tmplist.append(addstr)
            for dn in distrlist:
                teljari += 1
                if teljari == len(namelist):
                    tmplist.append(dn)
                    tmplist.append(", ")
                    tmplist.append("\n")
                    teljari = 0
                elif teljari != len(namelist):
                    tmplist.append(dn)
            for pnr in phonelist:
                teljari += 1
                if teljari == len(namelist):
                    tmplist.append(pnr)
                    tmplist.append(", ")
                    tmplist.append("\n")
                    teljari = 0
                elif teljari != len(namelist):
                    tmplist.append(pnr)

            allRestaulb = Label(allRestau, text="".join(tmplist), justify='left')
            allRestaulb.pack()
            allRestau.mainloop()

        elif str(var.get()) == 'Find by City name':
            rbcnSearch = Tk()  # restaurant by city name
            rbcnSearch.title('Hotel By City Name Search')
            rbcnSearch.geometry('200x100')

            Rname = Label(rbcnSearch, text='City name: ')
            Rname.grid(row=1, sticky=W)

            RnameE = Entry(rbcnSearch)
            RnameE.grid(row=1, column=1, sticky=W)

            def Restaurantsbycity():
                citynameentry = RnameE.get()
                rbcnSearch.destroy()
                restaurantbycitySearch = Tk()
                restaurantbycitySearch.title(citynameentry)
                restaurantbycitySearch.geometry('450x200')
                tmplist = []
                namelist = ["Hotel name: "]
                addresslist = ["Street Address: "]
                citylist = ["City: "]
                capacitylist = ["Max Capacity: "]
                websitelist = ["Website: "]
                restaurantbycity = restaurants.get_restaurant_by_city(citynameentry)
                for r in restaurantbycity:
                    restName = r[0] + ""
                    straddress = r[1] + ""
                    cityName = r[2] + ""
                    capacitynr = str(r[3]) + ""
                    website = r[4] + ""
                    namelist.append(restName)
                    addresslist.append(straddress)
                    citylist.append(cityName)
                    capacitylist.append(capacitynr)
                    websitelist.append(website)


                teljari = 0
                for rn in namelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(rn)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(rn)
                for addstr in addresslist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(addstr)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(addstr)
                for cn in citylist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(cn)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(cn)
                for cnr in capacitylist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(cnr)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(cnr)
                for weblink in websitelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(weblink)
                        tmplist.append(", ")
                        tmplist.append("\n")
                    elif teljari != len(namelist):
                        tmplist.append(weblink)

                rnsLab = Label(restaurantbycitySearch, text="".join(tmplist), justify='left')
                rnsLab.pack()
                restaurantbycitySearch.mainloop()

            searchB = Button(rbcnSearch, text='Search', command=Restaurantsbycity)
            searchB.grid(columnspan=2, sticky=W)

            rbcnSearch.mainloop()

        elif str(var.get()) == 'Find by District name':
            rbdnSearch = Tk()  # restaurant by district name
            rbdnSearch.title('Hotel By District Name Search')
            rbdnSearch.geometry('200x100')

            Rname = Label(rbdnSearch, text='City name: ')
            Rname.grid(row=1, sticky=W)

            RnameE = Entry(rbdnSearch)
            RnameE.grid(row=1, column=1, sticky=W)

            def Restaurantsbydistrict():
                districtnameentry = RnameE.get()
                rbdnSearch.destroy()
                restaurantbydistrictSearch = Tk()
                restaurantbydistrictSearch.title(districtnameentry)
                restaurantbydistrictSearch.geometry('450x200')
                tmplist = []
                namelist = ["Hotel name: "]
                addresslist = ["Street Address: "]
                citylist = ["City: "]
                capacitylist = ["Max Capacity: "]
                websitelist = ["Website: "]
                restaurantbydistrict = restaurants.get_restaurant_by_district(districtnameentry)
                for r in restaurantbydistrict:
                    restName = r[0] + ""
                    straddress = r[1] + ""
                    cityName = r[2] + ""
                    capacitynr = str(r[3]) + ""
                    website = r[4] + ""
                    namelist.append(restName)
                    addresslist.append(straddress)
                    citylist.append(cityName)
                    capacitylist.append(capacitynr)
                    websitelist.append(website)

                teljari = 0
                for rn in namelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(rn)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(rn)
                for addstr in addresslist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(addstr)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(addstr)
                for cn in citylist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(cn)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(cn)
                for cnr in capacitylist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(cnr)
                        tmplist.append(", ")
                        tmplist.append("\n")
                        teljari = 0
                    elif teljari != len(namelist):
                        tmplist.append(cnr)
                for weblink in websitelist:
                    teljari += 1
                    if teljari == len(namelist):
                        tmplist.append(weblink)
                        tmplist.append(", ")
                        tmplist.append("\n")
                    elif teljari != len(namelist):
                        tmplist.append(weblink)

                rnsLab = Label(restaurantbydistrictSearch, text="".join(tmplist), justify='left')
                rnsLab.pack()
                restaurantbydistrictSearch.mainloop()

            searchB = Button(rbdnSearch, text='Search', command=Restaurantsbydistrict)
            searchB.grid(columnspan=2, sticky=W)

            rbdnSearch.mainloop()

    button = Button(rootR, text="OK", command=showRestaurants)
    button.pack()

    rootR.mainloop()



Login()


