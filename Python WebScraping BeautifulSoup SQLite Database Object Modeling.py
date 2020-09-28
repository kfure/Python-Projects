'''
NF 510: Web Scraping, BeautifulSoup, SQLite Database, Object Modeling, Dictionaires

Webscraping NBA Draft basketball stats: my function will retrieve a URL for a specific year. The year is a parameter, so I can retrieve multiple pages/years. This function will retrieve the page, and return either the requests object for the page or the soup object. It will catch the relevant exceptions for when a webpage is not returned correctly.
The next function returns a data structure that contains a record for each player on the requested page. The information retrieved is:
first name
last name
url
college
team
points
year (see below)
The scraper functions are wrapped in a driver function that scrapes all years from 2003 through 2010.

Database and relation modeling design: store the information from my above functions in a database.

Database Design:
I have 4 tables: PLAYER, ANNUALSTATS, TEAMS and COLLEGES.
In the PLAYER table, I would have primary key id (integer), first name (string), last name (string),
foreign key college id (integer), and player link (string).
In the ANNUALSTATS table, I would have  a primary key id (integer), year (integer), foreign key
playerid (integer), foreign key team id (integer) and points(integer).
In the table TEAMS, I would have a primary key for id (integer) and the team name (string).
In the table COLLEGES, I would have a primary key for id (integer) and the college name (string).
You could join the tables to see all the data, but avoid storing duplicate string data,
such as player name, college, link and team name which could be repeated in the data.

Using Python, I Implement the schema outlined above, writed modularly. I can iterate across my player data structure, adding records to the database tables as appropriate.I check if an entry exists before I add a new row to avoid duplicates.
I iterate across my player structure to add all the information contained into the db schema I created above.

'''




import requests
from bs4 import BeautifulSoup
import sqlite3


d2 = {}
for y in range(2003, 2011):
    y = str(y)
    url = "http://www.basketball-reference.com/draft/NBA_"+ y +".html"
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print(f'Unable to retrieve data from website {url}.{err}.')
    else:
        soup = BeautifulSoup(r.content, 'lxml')
        main_table = soup.findAll('table', {"id" : "stats"})[0]
        main_body = main_table.find('tbody')
        year = soup.find('title').text[0:4]

        for player in main_body.findAll('tr'):
            if (len(player.findAll('td')) > 0):
                player_team = player.findAll('td')[1].find('a').attrs['title'].strip()
                player_name = player.findAll('td')[2].attrs['csk'].strip()
                lastname, firstname = player_name.split(',')
                player_link = player.findAll('td')[2].find('a')
                if (player_link != None):
                    player_link = player_link.attrs['href']
                else:
                     # If the link IS empty, assign the empty string
                    player_link = ''
                player_college = player.find('td', {'data-stat' : "college_name"}).attrs['csk'].strip()
                if player_college == 'Zzz':
                    player_college = ''
                player_points = player.findAll('td', {"data-stat" : "pts"})[0].text.strip()
                if player_points == '':
                    player_points = None
                play = []
                play.append(player_link)
                play.append(player_college)
                annual = []
                annual.append(year)
                annual.append(player_points)
                annual.append(player_team)
                d2[(lastname,firstname,player_link)] = play  #This will set the player link and college to the MOST RECENT year's data if there is a difference between years
                d2[lastname,firstname,player_link].append(annual) #This annual data will be appended for every year the player has a page
                    
    
    for k,v in d2.items():
        print(k,v)


def create_tables(cur):
    cur.execute('''DROP TABLE IF EXISTS Players''')
    cur.execute('''DROP TABLE IF EXISTS Annualstats''')
    cur.execute('''DROP TABLE IF EXISTS Teams''')
    cur.execute('''DROP TABLE IF EXISTS Colleges''')
    cur.execute('''CREATE TABLE Players (
                id integer PRIMARY KEY,
                lastname text,
                firstname text,
                link text,
                college_id integer)''')
    cur.execute('''CREATE TABLE Annualstats (
                        id integer PRIMARY KEY,
                        year integer,
                        points integer,
                        team_id integer,
                        player_id integer,
                        FOREIGN KEY (team_id) REFERENCES Teams(id)
                        FOREIGN KEY (player_id) REFERENCES Players(id))''')
    cur.execute('''CREATE TABLE Teams (
                        id integer PRIMARY KEY,
                        teamname TEXT UNIQUE)''')
    cur.execute('''CREATE TABLE Colleges (
                        id integer PRIMARY KEY,
                        college text UNIQUE)''')



conn = sqlite3.connect('nba_stats.sqlite')
cur = conn.cursor()
create_tables(cur)

''' Prepping and Inserting data into Colleges table
    Using d2 dictionary from Problem #1, which holds website data from 2003-2010.
    college - a temporary list being used to pull out all the colleges from the d2 dictionary data.
    collegeset - a set of the Colleges to verify a unique set of Colleges is being imported.
    dc - Creating a dictionary to store the primary key of each College to use as a 
    Foreign Key in other tables
    '''
colleges = []
dc = {}
for player1 in d2:
    if d2[player1][1] == '':
        d2[player1][1] = "None"   #If player has no college, default to "None"
    colleges.append(d2[player1][1])
collegeset = set(colleges)
for c in collegeset:
    sql = '''INSERT INTO Colleges (college) VALUES(?)'''
    cur.execute(sql,(c,))
    conn.commit()   
    foreign = cur.lastrowid
    dc[c] = foreign            #Stores college name as key to dc and foreign key as the corresponding value


sql_select_Query = '''select * from Colleges'''
cur.execute(sql_select_Query)
records = cur.fetchall()
for r in records:
    print(r)


''' Prepping and Inserting data into Teams table
    Using d2 dictionary from Problem #1, which holds website data from 2003-2010.
    teams - a temporary list being used to pull out all the teams from the d2 dictionary data.
    teamset - a set of the Teams to verify a unique set of Teams is being imported.
    dt - Creating a dictionary to store the primary key of each Team to use as a 
    Foreign Key in other tables
    '''
teams = []
dt = {}
for player1 in d2:
    if d2[player1][2][2] == '':
        d2[player1][2][2] = "None"
    print(d2[player1][2][2])
    teams.append(d2[player1][2][2])
teamset = set(teams)
print(teamset)


for t in teamset:
    sql = '''INSERT INTO Teams (teamname) VALUES(?)'''
    cur.execute(sql,(t,))
    conn.commit()   
    foreign = cur.lastrowid
    dt[t] = foreign


sql_select_Query1 = '''select * from Teams'''
cur.execute(sql_select_Query1)
records1 = cur.fetchall()
for r1 in records1:
    print(r1)


''' Inserting data into Players table
    Using d2 dictionary from Problem #1, which holds website data from 2003-2010.
    Using dc dictionary to get corresponding college foreign key for table insert data.
    dp - Creating a dictionary to store the primary key of each Player to use as a 
    Foreign Key in other tables
    '''
dp = {}
for p in d2:
    for_id = dc[d2[p][1]]
    sql = '''INSERT INTO Players (lastname, firstname, link, college_id) VALUES(?,?,?,?)'''
    cur.execute(sql,(p[0],p[1],d2[p][0],for_id,))
    conn.commit()   
    foreign = cur.lastrowid
    dp[p] = foreign


sql_select_Query2 = '''select * from Players'''
cur.execute(sql_select_Query2)
records2 = cur.fetchall()
for r2 in records2:
    print(r2)


''' Inserting data into Annualstats table
    Using d2 dictionary from Problem #1, which holds website data from 2003-2010.
    Using dt dictionary to get corresponding Team foreign key for table insert data. 
    Using dp dictionary to get corresponding Player foreign key for table insert data.
    '''
for p in d2:
    teamid = dt[d2[p][2][2]]
    playid = dp[p]
    sql = '''INSERT INTO Annualstats (year, points, team_id, player_id) VALUES(?,?,?,?)'''
    cur.execute(sql,(d2[p][2][0],d2[p][2][1],teamid,playid,))
    conn.commit()   



sql_select_Query2 = '''select * from Annualstats'''
cur.execute(sql_select_Query2)
records2 = cur.fetchall()
for r2 in records2:
    print(r2)

'''Checking table join for overall table data'''
sql_select_Query3 = '''
select Players.firstname, Players.lastname, Colleges.college, Annualstats.points, Annualstats.year, Teams.teamname
from Players 
join Colleges on Colleges.id = Players.college_id
join Annualstats on Players.id = Annualstats.player_id 
join Teams on Annualstats.team_id = Teams.id'''
cur.execute(sql_select_Query3)
records3 = cur.fetchall()
for r3 in records3:
    print(r3)


conn.close()


sql_select_Query5 = '''
select count(Players.id), Colleges.college
from Players 
join Colleges on Colleges.id = Players.college_id
where Colleges.college != "None"
group by Players.college_id
order by count() desc'''
cur.execute(sql_select_Query5)
records = cur.fetchall()
print(f'The university with the most players drafted between 2003 and 2010 was: \n\t{records[0][1]} with a total of {records[0][0]} players' )




sql_select_Query6 = '''
select Players.firstname, Players.lastname, Colleges.college
from Players 
inner join Colleges on Colleges.id = Players.college_id
where Players.firstname ='Chris' and Players.lastname = 'Paul' '''
cur.execute(sql_select_Query6)
record = cur.fetchall()
print(f'{record[0][0]} {record[0][1]} went to {record[0][2]} for college.')


sql_select_Query7 = '''
select Players.link
from Players 
left join Colleges on Colleges.id = Players.college_id
left join Annualstats on Players.id = Annualstats.player_id 
left join Teams on Annualstats.team_id = Teams.id
where Colleges.college = "UNC" and Teams.teamname LIKE 'Char%'
'''
cur.execute(sql_select_Query7)
rec = cur.fetchall()
print(f'The following links are for players who went to UNC for college and played for Charlotte \n at some point from 2003 to 2010.')
for r in rec:
    print(r[0])
      


sql_select_Query8 = '''
select sum(Annualstats.points), Annualstats.year
from Annualstats 
group by Annualstats.year
order by sum(points) desc'''
cur.execute(sql_select_Query8)
records = cur.fetchall()
print(f'The year with the most points was {records[0][1]} with {records[0][0]:,} total points!')