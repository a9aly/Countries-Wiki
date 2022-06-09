from bs4 import BeautifulSoup
import requests
import pymysql
import re

# Wikipedia link
WIKIPEDIA = 'https://en.wikipedia.org/'


# extract data from country pages
def country_crawler(country_link, tempCountryName, tempCountryCapital, capitalLink, tempContinent, cur):
    # country attributes
    language = ''
    population = ''
    drivingSide = ''
    continent = ''
    area = ''
    waterPercentage = ''
    callingCode = ''
    legislature = ''
    HDI = ''
    currency = ''
    GDPpp = ''
    GDPnominal = ''
    GiniIndex = ''
    president = ''
    linkPres = ''
    birthdate = ''
    officeDate = ''
    politicalParty = ''
    timezone = ''
    continent = tempContinent
    capitalArea = ''
    capitalGovernor = ''
    populationCapital = ''
    coordinatesCapital = ''
    # extract data needed country by country
    link = country_link
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'xml')
    countryTable = soup.findChild('table')
    # some countries data tables are not the first one, so there is a need to modify the current country table
    if countryTable.find('tr').find('th') is None:
        countryTable = countryTable.findNext('table')
    # extract country name
    countryName = tempCountryName

    # extract country capital
    capital = tempCountryCapital.replace("'", '`')

    # loop over 'tr' in country table
    for b in countryTable.findAll('tr'):
        text = b.find('th')
        if text is not None:
            # find language
            languageFind = text.getText().split('.')[0]
            if languageFind.find('Official language') != -1:
                if b.find('td').find('ul'):
                    for lis in b.find('td').find('ul').findAll('li'):
                        if lis.find('a') is not None:
                            if len(language) != 0:
                                language = language + ', ' + lis.find('a').get('title')
                            else:
                                language = lis.find('a').get('title')
                elif b.find('td').find('a') is not None :
                    language = b.find('td').find('a').get('title')
            elif languageFind.find('Official languages') != -1:
                if b.find('td').find('ul'):
                    for lis in b.find('td').find('ul').findAll('li'):
                        if lis.find('a') is not None:
                            if len(language) != 0:
                                language = language + ', ' + lis.find('a').get('title')
                            else:
                                language = lis.find('a').get('title')
                elif b.find('td').find('a'):
                    language = b.find('td').find('a').get('title')
                else:
                    language = b.find('td').getText()

            if languageFind == 'National language':
                if b.find('td').find('ul'):
                    for lis in b.find('td').find('ul').findAll('li'):
                        if lis.find('a') is not None:
                            if len(language) != 0:
                                language = language + ', ' + lis.find('a').get('title')
                            else:
                                language = lis.find('a').get('title')
                else:
                    language = b.find('td').find('a').get('title')

            # find population
            populationfind = text.getText().split('.')[0]
            if populationfind == 'Population':
                temp = b.find_next_sibling('tr').find('td', class_="infobox-data").getText().split('[')[0].split('\n')
                if countryName != 'Russia':
                    population = temp[0].split('(')[0].replace(' ', '')
                else:
                    population = temp[1].split('(')[0].replace(' ', '')

            # find Driving Side
            drivingSidefind = text.getText().split('.')[0]
            if drivingSidefind == 'Driving side':
                drivingSide = b.find('td').getText().split('[')[0]


            # find calling code
            callingCodefind = text.getText().split('.')[0]
            if callingCodefind == 'Calling code':
                callingCode = b.find('td').getText().split('[')[0]

            # find Area and water %
            areafind = text.getText().split('.')[0]
            if areafind.find('Area') != -1:
                area = b.find_next_sibling('tr').find('td').getText().split('(')[0]
                # remove [] from country space
                for z in range(2):
                    if area.find('[') != -1:
                        start = area.find('[')
                        end = area.find(']')
                        area = area[0:start:] + area[end+1::]

            waterPercentagefind = text.getText()
            if waterPercentagefind.find('Water') != -1:
                waterPercentage = b.find('td').getText().split('[')[0].split(' ')[0]
                if waterPercentage.find('%') == -1 and waterPercentage.find('egligible') == -1:
                    waterPercentage = waterPercentage + '%'
            # find Legislature
            legislaturefind = text.getText().split('.')[0]
            if legislaturefind == 'Legislature':
                legislature = b.find('td').getText().replace("'", "`").split('[')[0]

            # find HDI
            HDIfind = text.getText().split('.')[0]
            if HDIfind.find('HDI') != -1:
                HDI = b.find('td').getText().split('[')[0].replace('\xa0', '')

            # find currency
            currencyfind = text.getText()
            if currencyfind.find('Currency') != -1:
                currency = b.find('td').getText().split('[')[0].replace("'", "`").replace("\n", " ")

            # find GDP PP and GDP NOMINAL
            GDPfind = text.getText().split('.')[0]
            if GDPfind.find('GDP') != -1:
                if GDPpp == '':
                    GDPpp = b.find('td').findNext().getText().split('[')[0].replace('• Total', '').split('(')[0]
                else:
                    GDPnominal = b.find('td').findNext().getText().split('[')[0].replace('• Total', '')

            # find GiniIndex
            GiniIndexfind = text.getText().split('.')[0]
            if countryName == 'Papua New Guinea':
                if GiniIndexfind.find('Gini (') != -1:
                    GiniIndex = b.find('td').getText().split('[')[0].replace(" ", '')
            elif GiniIndexfind.find('Gini') != -1:
                GiniIndex = b.find('td').getText().split('[')[0].replace(" ", "")

            # find timezone
            timezonefind = text.getText().split('.')[0]
            if timezonefind == 'Time zone':
                timezone = b.find('td').getText().split('[')[0]
            if timezonefind.find('Summer') != -1:
                timezone = timezone + ', Summer: ' + b.find('td').getText()

            # find president
            presidentfind = text.getText().split('.')[0]
            if president == '' and capital != 'Sukhumi' and countryName != 'South Ossetia' and countryName != 'Northern Cyprus':
                if presidentfind == 'Government':
                    president = b.findNext('tr').findNext('tr').find('td').find('a').get('title')
                    linkPres = WIKIPEDIA + b.findNext('tr').findNext('tr').find('td').find('a').get('href')

    # find president data
    if linkPres != '':
        page2 = requests.get(linkPres)
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        presidentTable = soup2.findChild('table', class_="infobox")
        if presidentTable is not None:
            for c in presidentTable.findAll('tr'):
                text2 = c.find('th')
                # get birthdate
                if text2 is not None:
                    birthdatefind = text2.getText().split('.')[0]
                    if birthdatefind == 'Born':
                        if c.find('td').find('span', class_="bday"):
                            birthdate = c.find('td').find('span', class_="bday").getText()
                        elif c.find('td', 'class="infobox-data"'):
                            birthdate = c.find('td', 'class="infobox-data"').getText().split('(')[0]

                # get office date
                text2 = c.find('td')
                if officeDate == '':
                    if text2 is not None:
                        officeDatefind = text2.getText()
                        if officeDatefind.find('Assumed office') != -1:
                            officeDate = officeDatefind[15:]

                    text2 = c.find('th')
                    if text2 is not None:
                        officeDatefind = text2.getText()
                        if officeDatefind.find('Reign') != -1:
                            officeDate = c.find('td').getText().split('&nbsp')[0][:-10]

                #get political party
                if politicalParty == '':
                    text2 = c.find('th')
                    if text2 is not None:
                        politicalPartyfind = text2.getText()
                        if politicalPartyfind.find('Political party') != -1:
                            if c.find('td').find('a') is not None:
                                politicalParty = c.find('td').find('a').getText().replace("'", "`")

    # find capital data
    if capitalLink != '':
        page3 = requests.get(capitalLink)
        soup3 = BeautifulSoup(page3.content, 'html.parser')
        capitalTable = soup3.findChild('table', class_="infobox ib-settlement vcard")
        if capitalTable is not None:
            for d in capitalTable.findAll('tr'):
                text3 = d.find('th')
                # get capital population
                if text3 is not None:
                    findPopulationCapital = text3.getText()
                    if findPopulationCapital.find('Population') != -1:
                        temp = d.findNext('tr').find('td')
                        if temp is not None:
                            populationCapital = temp.getText().split('[')[0]

                    findAreaCapital = text3.getText()
                    if findAreaCapital.find('Area') != -1:
                        temp = d.findNext('tr').find('td')
                        if temp is not None and capitalArea == '':
                            capitalArea = temp.getText().split(' ')[0]

                    findAreaGovernor = text3.getText()
                    if findAreaGovernor.find('Government') != -1:
                            temp = d.findNext('tr').find('td')
                            if temp is not None and capitalGovernor == '':
                                if d.findNext('th').findNext('th').getText().find('Type') != -1:
                                    if d.findNext('th').findNext('th').findNext('th').getText().find('Body') != -1:
                                        temp = temp.findNext('tr').findNext('tr').find('td')
                                        if temp is not None:
                                            capitalGovernor = temp.getText().split('(')[0].split('[')[0]
                                    else:
                                        capitalGovernor = temp.getText().split('(')[0].split('[')[0]
                                elif capitalGovernor == '':
                                    capitalGovernor = temp.getText().split('(')[0].split('[')[0]

                text4 = d
                if text4 is not None:
                    findCapitalCoordinate = text4.getText()
                    if findCapitalCoordinate.find('Coordinates') != -1:
                        if d.find('span', class_="plainlinks nourlexpansion").find('a', class_="external text") is not None:
                            #coordinatesCapital = d.find('span.latitude').getText() + d.find('span.longtitude').getText()
                            if d.find('span', 'latitude') is not None:
                                coordinatesCapital = d.find('span', 'latitude').getText()
                            if d.find('span', 'longitude') is not None:
                                coordinatesCapital = coordinatesCapital + ' ' + d.find('span', 'longitude').getText()


    instruction3 = f"INSERT IGNORE INTO presidentmonarch (Name, Birthdate, OfficeDate, PoliticalParty) VALUES ('{president}', '{birthdate}', '{officeDate}', '{politicalParty}')"
    cur.execute(instruction3)
    instruction2 = f"INSERT IGNORE INTO capital (Name, Population, Area, Governor, Coordinates) VALUES ('{capital}', '{populationCapital}', '{capitalArea}', '{capitalGovernor}', '{coordinatesCapital}')"
    cur.execute(instruction2)
    instruction = f"INSERT IGNORE INTO country (Name,officialLanguage, Population, DrivingSide, CallingCode, Area, Legislature, WaterPercentage, HDI, Currency, GDP_PurchasePower, GDP_Nominal, capital_Name, GiniIndex, timeZone, president_monrach_Name, Continent) VALUES ('{countryName}', '{language}','{population}', '{drivingSide}', '{callingCode}', '{area}', '{legislature}', '{waterPercentage}', '{HDI}', '{currency}', '{GDPpp}', '{GDPnominal}', '{capital}', '{GiniIndex}', '{timezone}', '{president}', '{continent}')"
    cur.execute(instruction)


# start mysql server and assign server data
def start_mysql():
    # MYSQL Server Details
    Host = 'localhost'
    User = 'root'
    Password = 'Your Server Password'
    database = 'world_geopedia_system'
    # connect to mysql server
    conn = pymysql.connect(host=Host, user=User, password=Password, database=database)
    # Create a cursor object
    cur = conn.cursor()
    return conn, cur


# extract country wikipedia links
def get_country_name(conn,cur):
    z = 1
    # 1- Africa
    page2 = requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Africa")
    soup2 = BeautifulSoup(page2.content, 'xml')
    continentTable = soup2.findChild('table', class_="wikitable sortable")
    if continentTable is not None:
        continentTable = continentTable.find('tbody')
        for n in continentTable.findAll('tr'):
            if n.find('td'):
                tempCountryLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find('a').get('href')
                tempCountryName = n.find('td').find('a').find_next('td').find_next('td').find('a').get('title')
                tempCountryCapital = n.find('td').find('a').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('title')
                cityLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href')
                print(z)
                country_crawler(tempCountryLink, tempCountryName, tempCountryCapital, cityLink, 'Africa', cur)
                z=z+1

    # 2- South_America
    page2 = requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_South_America")
    soup2 = BeautifulSoup(page2.content, 'xml')
    continentTable = soup2.findChild('table', class_="wikitable sortable")
    if continentTable is not None:
        continentTable = continentTable.find('tbody')
        for n in continentTable.findAll('tr'):
            if n.find('td'):
                tempCountryLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find('a').get('href')
                tempCountryName = n.find('td').find('a').find_next('td').find_next('td').find('a').get('title')
                tempCountryCapital = n.find('td').find('a').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('title')
                cityLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href')
                print(z)
                country_crawler(tempCountryLink, tempCountryName, tempCountryCapital, cityLink, 'South America', cur)
                z = z + 1

    # 3- Europe
    page2 = requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Europe")
    soup2 = BeautifulSoup(page2.content, 'xml')
    continentTable = soup2.findChild('table', class_="wikitable sortable")
    if continentTable is not None:
        continentTable = continentTable.find('tbody')
        for n in continentTable.findAll('tr'):
            if n.find('td'):
                tempCountryLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find('a').get('href')
                tempCountryName = n.find('td').find('a').find_next('td').find_next('td').find('a').get('title')
                tempCountryCapital = n.find('td').find('a').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('title')
                cityLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href')
                print(z)
                country_crawler(tempCountryLink, tempCountryName, tempCountryCapital, cityLink, 'Europe', cur)
                z = z + 1

    # 4- ASIA
    page2 = requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Asia")
    soup2 = BeautifulSoup(page2.content, 'xml')
    continentTables = soup2.findAll('table', class_="wikitable sortable")
    i = 1
    for continentTable in continentTables:
        if continentTable is not None:
            continentTable = continentTable.find('tbody')
            for n in continentTable.findAll('tr'):
                if n.find('td') and i == 1:
                    tempCountryLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find('a').get('href')
                    tempCountryName = n.find('td').find_next('td').find_next('td').find('a').get('title')
                    tempCountryCapital = n.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('title')
                    cityLink = WIKIPEDIA + n.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href')
                    print(z)
                    country_crawler(tempCountryLink, tempCountryName, tempCountryCapital, cityLink, 'Asia', cur)
                    z = z + 1


                elif n.find('td') and i != 1:
                    tempCountryLink = WIKIPEDIA + n.find('td').find_next('td').find_next('td').find_next('td').find('a').get('href')
                    tempCountryName = n.find('td').find_next('td').find_next('td').find('a').get('title')
                    tempCountryCapital = n.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('title')
                    cityLink = WIKIPEDIA + n.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href')
                    print(z)
                    country_crawler(tempCountryLink, tempCountryName, tempCountryCapital, cityLink, 'Asia', cur)
                    z = z + 1
            i = i+1

    # 5- North America
    page2 = requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_North_America")
    soup2 = BeautifulSoup(page2.content, 'xml')
    continentTable = soup2.findChild('table', class_="wikitable sortable")
    if continentTable is not None:
        continentTable = continentTable.find('tbody')
        for n in continentTable.findAll('tr'):
            if n.find('td'):
                tempCountryLink = WIKIPEDIA + n.find('td').find_next('td').find('a').get('href')
                tempCountryName = n.find('td').find_next('td').find('a').get('title')
                tempCountryCapital = n.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('title')
                cityLink = WIKIPEDIA + n.find('td').find('a').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href')
                print(z)
                country_crawler(tempCountryLink, tempCountryName, tempCountryCapital, cityLink, 'North America', cur)
                z = z + 1

    fill_user_database(cur)


# fill user database with random data
def fill_user_database(cur):
    usernames = ['chardonnayflores', 'leodaugherty', 'natanielrankin', 'evamcknight', 'arifdoherty', 'caironhartman', 'zaaracoates', 'owensumner', 'sabinadaly', 'amaliabeach', 'bentleyalston', 'esmemillington', 'mia-rosecollins', 'liliannaburch', 'serenitymarin', 'kathrynkirkpatrick', 'ernestlott', 'gurveerburns', 'radhikalowe', 'kayleighspencer', 'carmenrayner', 'duncanschroeder', 'addiehassan', 'kolefirth', 'sidrabradshaw', 'abdulrahmanrodgers', 'stanleygill', 'usmaanmolloy', 'yvettegriffin', 'percysheehan', 'asmagriffith', 'fentonsutherland', 'myshaali', 'bethaneynoel', 'tariqmills', 'samiapeterson', 'sohailsouthern', 'poppiemac', 'albydecker', 'pixiecase', 'jaidenwooten', 'aarondavila', 'gretaduran', 'deliaferguson', 'tulisalyon', 'willowmontes', 'nualareynolds', 'shauryawoodley', 'catrincullen', 'simeonchamberlain']
    gender = ['m'] * 25 + ['f'] * 25
    emails = ['maneesh@gmail.com', 'gerlo@live.com', 'druschel@msn.com', 'stakasa@mac.com', 'ilyaz@verizon.net', 'jfriedl@live.com', 'jgmyers@verizon.net', 'satishr@verizon.net', 'peterhoeg@yahoo.ca', 'pedwards@icloud.com', 'kayvonf@aol.com', 'pierce@mac.com', 'kaiser@msn.com', 'ntegrity@aol.com', 'paley@att.net', 'retoh@sbcglobal.net', 'manuals@outlook.com', 'mjewell@gmail.com', 'liedra@aol.com', 'madanm@msn.com', 'caronni@aol.com', 'breegster@live.com', 'flakeg@gmail.com', 'brainless@me.com', 'maikelnai@sbcglobal.net', 'agapow@aol.com', 'amaranth@optonline.net', 'treit@aol.com', 'oechslin@gmail.com', 'unreal@aol.com', 'hellfire@mac.com', 'sokol@hotmail.com', 'arebenti@icloud.com', 'drolsky@mac.com', 'yamla@gmail.com', 'jrkorson@optonline.net', 'notaprguy@verizon.net', 'paulv@verizon.net', 'fmtbebuck@comcast.net', 'gravyface@icloud.com', 'hellfire@me.com', 'sonnen@hotmail.com', 'dmouse@aol.com', 'stewwy@yahoo.com', 'jbuchana@live.com', 'naupa@msn.com', 'kannan@yahoo.com', 'dalamb@outlook.com', 'denism@att.net', 'grady@comcast.net']
    ages = [40, 23, 19, 53, 41, 48, 18, 27, 50, 20, 36, 32, 55, 44, 38, 30, 34, 38, 16, 37, 16, 47, 26, 17, 35, 37, 37, 41, 54, 43, 60, 17, 25, 53, 30, 33, 56, 16, 34, 56, 22, 51, 38, 31, 18, 34, 30, 50, 17, 19]
    birthdates = ['1972-03-23', '1966-09-27', '1965-07-23', '1970-07-09', '1981-07-29', '1964-07-09', '1966-01-03', '1965-08-06', '1989-08-05', '1961-06-28', '1985-10-12', '1998-05-16', '1963-03-04', '1991-03-14', '1974-01-11', '1984-09-23', '1963-05-17', '1964-02-12', '1989-05-11', '1966-05-07', '1961-01-19', '1965-09-21', '2001-06-30', '1995-08-29', '1976-01-11', '1995-10-02', '1992-08-15', '1987-02-19', '1977-04-25', '1969-07-03', '1999-08-14', '1977-09-22', '1989-11-11', '1979-09-01', '1997-11-27', '1975-01-22', '1960-12-19', '1977-08-23', '1967-01-01', '1975-09-11', '1968-05-15', '1974-04-03', '1981-04-24', '1966-05-14', '1995-08-31', '1961-07-08', '1985-04-18', '1968-11-14', '1967-07-12', '1992-01-19']
    countriesVisited = ['Egypt', 'Djibouti', 'Belgium', 'Zambia', 'Morocco', 'Italy', 'Saint Kitts and Nevis', 'Brazil', 'Cuba', 'Singapore', 'Slovakia', 'Australia', 'Qatar', 'Swaziland', 'Israel', 'Libya', 'Nicaragua', 'South Korea', 'Niger', 'Isle of Man', 'Guam', 'France', 'New Zealand', 'Andorra', 'Kyrgyzstan', 'Saint Barthelemy', 'Japan', 'American Samoa', 'Cyprus', 'Bhutan', 'Iraq', 'South Africa', 'Malta', 'Papua New Guinea', 'Moldova', 'Angola', 'El Salvador', 'Algeria', 'Zimbabwe', 'Democratic Republic of the Congo', 'Sierra Leone', 'Cook Islands', 'Northern Mariana Islands', 'Ukraine', 'Philippines', 'Peru', 'Nigeria', 'Bonaire', 'Cayman Islands', 'Hong Kong']
    arrivaldates = ['2018-01-07', '2018-07-16', '2017-12-23', '2020-01-19', '2019-04-26', '2017-03-11', '2016-03-21', '2020-12-21', '2016-08-17', '2018-08-01', '2019-04-24', '2017-03-06', '2021-01-20', '2015-07-25', '2019-08-31', '2015-12-13', '2015-07-04', '2015-04-28', '2017-03-06', '2018-01-04', '2018-02-16', '2016-02-12', '2018-03-25', '2015-12-22', '2021-08-12', '2016-04-30', '2015-04-05', '2021-05-13', '2019-03-06', '2017-02-02', '2021-03-09', '2018-07-09', '2019-10-02', '2021-09-09', '2019-03-14', '2020-06-08', '2015-09-19', '2018-12-29', '2020-05-09', '2016-10-26', '2018-01-31', '2021-10-11', '2018-10-13', '2017-06-22', '2021-03-25', '2016-02-17', '2019-08-03', '2019-08-20', '2020-05-03', '2017-03-08']
    departuredates = ['2018-02-18', '2019-11-15', '2018-08-12', '2015-03-05', '2021-05-19', '2017-03-28', '2021-05-21', '2017-12-12', '2016-12-04', '2021-03-08', '2019-12-10', '2015-12-10', '2021-08-26', '2018-04-15', '2021-01-21', '2016-07-10', '2016-08-20', '2020-06-16', '2020-11-19', '2018-01-31', '2021-02-08', '2018-03-13', '2015-03-14', '2015-11-12', '2016-01-21', '2020-04-28', '2018-02-13', '2017-01-04', '2020-02-09', '2021-07-30', '2019-09-27', '2016-04-28', '2017-04-17', '2015-09-26', '2019-03-12', '2020-10-02', '2021-10-17', '2021-01-09', '2019-03-18', '2015-06-13', '2020-10-04', '2017-07-01', '2015-06-14', '2019-10-28', '2016-01-08', '2018-01-12', '2021-04-04', '2019-09-06', '2018-01-24', '2017-05-19']
    rating = [1, 2, 1, 9, 7, 9, 7, 3, 4, 7, 8, 5, 9, 3, 5, 9, 2, 8, 5, 3, 1, 2, 3, 5, 5, 1, 7, 8, 5, 6, 3, 7, 1, 9, 9, 5, 3, 1, 7, 6, 8, 8, 2, 1, 4, 7, 1, 6, 8, 2]
    textualReview = ['excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'excellent will visit it again', 'poor experience', 'poor experience', 'poor experience', 'poor experience', 'poor experience', 'poor experience', 'poor experience', 'poor experience', 'poor experience', 'poor experience', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again', 'will visit again']
    for i in range(50):
        instruction5 = f"INSERT IGNORE INTO users (EmailAddress, UserName, Gender, Age, BirthDate, VisitedCountry, ArrivalDate, DepartureDate, Rating_1out10, TextualReview) VALUES ('{emails[i]}', '{usernames[i]}', '{gender[i]}', '{ages[i]}', '{birthdates[i]}', '{countriesVisited[i]}', '{arrivaldates[i]}', '{departuredates[i]}', '{rating[i]}', '{textualReview[i]}')"
        cur.execute(instruction5)


# insert all attributes into database
def end_mysql(conn):
    conn.commit()
    conn.close()


def main():
    conn, cur = start_mysql()
    get_country_name(conn, cur)
    end_mysql(conn)


if __name__ == "__main__":
    main()