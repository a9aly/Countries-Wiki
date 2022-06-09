import pymysql
import re
import phonenumbers


def add_user():
    EmailAddress = input('Enter your email in this format ahmed@example.com: ')
    UserName = input('Enter your username: ')
    Gender = input('Gender m for Male - f for female: ')
    Age = input('Enter Age: ')
    BirthDate = input('Enter your birthdate YYYY-MM-DD: ')
    VisitedCountry = input('Enter country you visited: ')
    ArrivalDate = input('Enter date you visited a country YYYY-MM-DD: ')
    DepartureDate = input('Enter date you departured a country YYYY-MM-DD: ')
    Rating_1out10 = input('Enter rating from 1:10: ')
    TextualReview = input('Enter text review: ')
    add_user = f'''INSERT INTO `users`(`EmailAddress`, `UserName`, `Gender`, `Age`, `BirthDate`, `VisitedCountry`, `ArrivalDate`, `DepartureDate`, `Rating_1out10`, `TextualReview`) VALUES ("{EmailAddress}","{UserName}","{Gender}","{Age}","{BirthDate}","{VisitedCountry}","{ArrivalDate}","{DepartureDate}","{Rating_1out10}","{TextualReview}")'''
    cursor.execute(add_user)

def view_country_reviews():
    country = input('Enter country name ')
    selectCountry = f'SELECT `EmailAddress`, `UserName`, `Gender`, `Age`, `BirthDate`, `VisitedCountry`, `ArrivalDate`, `DepartureDate`, `Rating_1out10`, `TextualReview` FROM `users` WHERE `VisitedCountry` = "{country}"'
    cursor.execute(selectCountry)
    reviews = cursor.fetchall()
    i = 1
    for review in reviews:
        print("Review Number:", i)
        print("Email:", review[0])
        print("Username:", review[1])
        print("Gender:", review[2])
        print("Age:", review[3])
        print("Birthdate:", review[4])
        print("Visited Country:", review[5])
        print("Arrival Date:", review[6])
        print("Departure Date:", review[7])
        print("Raring:", review[8])
        print("Textual Review:", review[9])
        i = i+1
        print(" ")


def get_legislature():
    legislature = input("Enter legislature required: ")
    selectlegislature = f'SELECT Name FROM country WHERE Legislature = "{legislature}"'
    cursor.execute(selectlegislature)
    legislatures = cursor.fetchall()
    for legislature in legislatures:
        print("Country Name:", legislature[0])


def get_top_countries():
    continentORcountries = int(input('Enter 1 to Pick top countries according to continent otherwise enter any other number: '))
    if continentORcountries != 1:
        gdp = 'SELECT Name, GDP_PurchasePower FROM country ORDER BY GDP_PurchasePower DESC LIMIT 10'
        cursor.execute(gdp)
        fetchs = cursor.fetchall()
        print("Top 10 countries by GDP Purchase Power")
        for fetch in fetchs:
            print("Country:", fetch[0], " GDP Purchase Power:", fetch[1])
        print(" ")

        pop ='SELECT Name, Population FROM country ORDER BY Population DESC LIMIT 10'
        cursor.execute(pop)
        fetchs = cursor.fetchall()
        print("Top 10 countries by population")
        for fetch in fetchs:
            print("Country:", fetch[0], " Population:", fetch[1])
        print(" ")

        area = 'SELECT Name, Area FROM country ORDER BY Area DESC LIMIT 10'
        cursor.execute(area)
        fetchs = cursor.fetchall()
        print("Top 10 countries by area")
        for fetch in fetchs:
            print("Country:", fetch[0], " Area:", fetch[1])
        print(" ")

        populArea = 'SELECT Name,Population, Area FROM country ORDER BY Population/Area DESC LIMIT 10'
        cursor.execute(populArea)
        fetchs = cursor.fetchall()
        print("Top 10 countries by density")
        for fetch in fetchs:
            print("Country:", fetch[0], " Population: ", fetch[1], " Area:", fetch[2])
        print(" ")

        gdpperPop = 'SELECT Name,GDP_PurchasePower,Population FROM country ORDER BY GDP_PurchasePower/Population DESC LIMIT 10'
        cursor.execute(gdpperPop)
        fetchs = cursor.fetchall()
        print("Top 10 countries by GDP per capital")
        for fetch in fetchs:
            print("Country:", fetch[0], " GDP Purchase Power ", fetch[1], "Population: ", fetch[2])
        print(" ")

    else:
        get_top_countries_continent()


def get_top_countries_continent():
    continent = input("Enter continent Name: ")
    gdp = f'SELECT Name, GDP_PurchasePower FROM country WHERE Continent = "{continent}" ORDER BY GDP_PurchasePower DESC LIMIT 10'
    cursor.execute(gdp)
    fetchs = cursor.fetchall()
    print("Top 10 countries by GDP Purchase Power")
    for fetch in fetchs:
        print("Country:", fetch[0], " GDP Purchase Power:", fetch[1])
    print(" ")

    pop = f'SELECT Name, Population FROM country WHERE Continent = "{continent}" ORDER BY Population DESC LIMIT 10'
    cursor.execute(pop)
    fetchs = cursor.fetchall()
    print("Top 10 countries by population")
    for fetch in fetchs:
        print("Country:", fetch[0], " Population:", fetch[1])
    print(" ")

    area = f'SELECT Name, Area FROM country WHERE Continent = "{continent}" ORDER BY Area DESC LIMIT 10'
    cursor.execute(area)
    fetchs = cursor.fetchall()
    print("Top 10 countries by area")
    for fetch in fetchs:
        print("Country:", fetch[0], " Area:", fetch[1])
    print(" ")

    populArea = f'SELECT Name,Population, Area FROM country WHERE Continent = "{continent}" ORDER BY Population/Area DESC LIMIT 10'
    cursor.execute(populArea)
    fetchs = cursor.fetchall()
    print("Top 10 countries by density")
    for fetch in fetchs:
        print("Country:", fetch[0], " Population: ", fetch[1], " Area:", fetch[2])
    print(" ")

    gdpperPop = f'SELECT Name,GDP_PurchasePower,Population FROM country WHERE Continent = "{continent}" ORDER BY GDP_PurchasePower/Population DESC LIMIT 10'
    cursor.execute(gdpperPop)
    fetchs = cursor.fetchall()
    for fetch in fetchs:
        print("Country:", fetch[0], " GDP Purchase Power ", fetch[1], "Population: ", fetch[2])
    print(" ")


def get_right_left():
    direction = int(input('1-right, 2-left: '))
    if direction == 1:
        cursor.execute("SELECT Name FROM country WHERE DrivingSide = 'right'")
        fetchs = cursor.fetchall()
        for fetch in fetchs:
            print('Country Name:', fetch[0])

    elif direction == 2:
        cursor.execute("SELECT Name FROM country WHERE DrivingSide = 'left'")
        fetchs = cursor.fetchall()
        for fetch in fetchs:
            print('Country Name:', fetch[0])


def get_capitalcountry():
    countryORcapital = int(input('1-Country, 2-Capital: '))
    if countryORcapital == 1:
        country = input('Enter Country Name to retrieve its Data: ')
        cursor.execute(f'SELECT * FROM country WHERE Name = "{country}"')
        fetchs = cursor.fetchall()
        for fetch in fetchs:
            print('Name:', fetch[0])
            print('Population:', fetch[1])
            print('Driving Side:', fetch[2])
            print('Calling Code:', fetch[3])
            print('Continent:', fetch[4])
            print('Area:', fetch[5])
            print('Water Population:', fetch[6])
            print('Legislature:', fetch[7])
            print('HDI:', fetch[8])
            print('Currency:', fetch[9])
            print('GDP Purchase:', fetch[10])
            print('GDP Nominal:', fetch[11])
            print('Gini Index:', fetch[12])
            print('Time Zone:',fetch[13])
            print('Official Language:', fetch[14])
            print('Capital Name:', fetch[15])
            print('President Monarch/Name:', fetch[16])
    elif countryORcapital == 2:
        capital = input('Enter Capital Name to retrieve its Data: ')
        cursor.execute(f'SELECT * FROM capital WHERE Name = "{capital}"')
        fetchs = cursor.fetchall()
        for fetch in fetchs:
            print('Name:', fetch[0])
            print('Population:', fetch[1])
            print('Area:', fetch[2])
            print('Governor:', fetch[3])
            print('Coordinates:', fetch[4])


def get_president():
    president = input('Enter President/Monarch name: ')
    #president = 'Abdel Fattah el-Sisi'
    cursor.execute(f'SELECT * FROM presidentmonarch WHERE Name = "{president}"')
    fetchs = cursor.fetchall()
    for fetch in fetchs:
        print('Name:', fetch[0])
        print('Birthdate:', fetch[1])
        print('Office Date:', fetch[2])
        print('Political Party:', fetch[3])


def get_phone_country():
    source = input('Enter phone number: ')
    temp = phonenumbers.parse(source, None)
    phone = '+' + str(temp.country_code)
    print(phone)
    cursor.execute(f"SELECT Name FROM country WHERE CallingCode= '{phone}'")
    fetchs = cursor.fetchall()
    for fetch in fetchs:
        print("Country with code", phone, ' is:', fetch[0])


def get_country():
    city = input('Enter city Name:')
    cursor.execute(f"SELECT Name FROM country WHERE  capital_Name =  '{city}'")
    fetchs = cursor.fetchall()
    for fetch in fetchs:
        print("Country Name is:", fetch[0])


def menu():
    print("Welcome to World Geopedia")
    ans = 1
    while ans != 0:
        print('1 - Add a new user review on a country')
        print('2 - View existing reviews on a given country')
        print('3 - Show all the countries that have a specific legislature')
        print('4 - Show the top 10 countries by GDP, population, area, density, GDP per capita, both globally and within each continent')
        print('5 - Show all the countries who drive on the right vs. on the left')
        print('6 - Query and view a given country / capital city information')
        print('7 - Query and view president / monarch’s information')
        print('8 - Identify the country for a given phone number')
        print('9 - Identify the country of a given city')
        print('0 - Close the program')
        ans = int(input("Pick your choice from above "))
        if ans == 1:
            add_user()
        elif ans == 2:
            view_country_reviews()
        elif ans == 3:
            get_legislature()
        elif ans == 4:
            get_top_countries()
        elif ans == 5:
            get_right_left()
        elif ans == 6:
            get_capitalcountry()
        elif ans == 7:
            get_president()
        elif ans == 8:
            get_phone_country()
        elif ans == 9:
            get_country()


if __name__ == '__main__':
    connection = pymysql.connect(host="www.db4free.net", user="ahmedali9", passwd="AhmedAli99", database="world_geo")
    cursor = connection.cursor()
    menu()
    connection.commit()
    connection.close()

