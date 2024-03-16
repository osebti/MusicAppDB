import sqlite3
from sys import argv
from getpass import getpass

conn = sqlite3.connect(argv[1])
c = conn.cursor()
c.execute('	PRAGMA	foreign_keys=ON;	')

userID: str # variables used to handle session activities/functions 
sessionNum = -1
artist: bool = False
loggedIn: bool = False


def parse(inp: str): #parsing function that determines input-function binds
    inp = inp.strip()  # remove whitespace
    if inp == "ssp" and not artist:
        searchKeywordSong()
    elif inp == "start" and not artist:
        if sessionNum != -1:
            print("\nThere is already an ongoing session. To start a new session enter 'end' to end this current session.\n")
        else:
            startSession()
    elif inp == "exit":
        exitProgram()
    elif inp == "end" and not artist:
        if sessionNum == -1:
            print(
                "\nThere is currently no ongoing session. To start a new session enter 'start'.\n")
        else:
            endSession()
        return
    elif inp == "sa" and not artist:
        keywordArtist()
        return
    elif inp == "top" and artist == True:
        topFansPl()
    elif inp == "logout":
        logout()
        return
    elif inp == "add" and artist == True:
        try:
            inp1 = input("type the song title: ")
            inp2 = input("type the song duration: ")
            inp1=str(inp1)
            inp2=int(inp2)
            addSong(inp1, inp2)
            return

        except:
            print("invalid input(s) or invalid aid, unable to perform operation")
            return
    else:
        print("invalid input\n")
    return


def logout(): # logout function that resets to default tracking variables and return user to login page
    global sessionNum, artist, userID, loggedIn
    endSession()
    sessionNum = -1  # reset everything to default
    artist = False
    userID = ""
    loggedIn = False
    return


def userSession():  # user command loop
    while (loggedIn):
        print("------------------------------------------------MENU-----------------------------------------------")
        print("--[type 'start' to start a listening session]")
        print("--[type 'ssp' to search for a playlist or song]")
        print("--[type 'exit' to exit and close the program]")
        print("--[type 'end' to end the current session]")
        print("--[type 'sa' to search for an artist]")
        print("--[type 'logout' to log out]")
        inp = input("enter your command: ")
        inp.strip()
        parse(inp)
    return


def artistSession():  # artist command loop
    while (loggedIn):
        print("------------------------------------------------MENU-----------------------------------------------")
        print("--[type 'add' to add a song]")
        print("--[type 'top' to find top fans and playlists]")
        print("--[type 'logout' to log out]")
        print("--[type 'exit' to exit and close the program]")
        inp = input("enter your command:")
        inp.strip()
        parse(inp) # call parse to map input to function


def login():
    global artist, loggedIn, userID # set to global to make changes visible everywhere
    while (True):
        print("\n-----LOGIN-----")
        inp = input("[press 'l' to login] or [press 's' to sign up]: ") # login prompt
        inp = str(inp)
        inp = inp.strip()

        if inp == 'l': # login handling block
            uid = (input("username: ").strip())
            uid=str(uid)
            id=uid.upper()
            pwd = getpass("password: ").strip() # non-visible pass and queries to get uid,pwd combos
            c.execute('''
            select uid,pwd
            from users
            where upper(uid)=?
            and pwd=?;
            ''', (id, pwd))
            row1 = c.fetchone()

            c.execute('''
            select aid,pwd
            from artists
            where upper(aid)=?
            and pwd=?;
            ''', (id, pwd))

            row2 = c.fetchone()

            if row1 != None and row2 != None: # check if uid is not also an aid 
                inp = input(
                    "press 'a' to login as artist, 'u' to login as user: ").strip()
                if (inp == 'a'):
                    artist = True
                    loggedIn = True
                    userID = uid
                    artistSession()

                elif inp == 'u':
                    loggedIn = True
                    userID = uid
                    userSession()  # generate the ui frame for the user
                elif inp == 'exit':
                    exit()
                else:
                    print("invalid command, try login again")

            elif (row1 != None):
                loggedIn = True
                userID = uid
                userSession()

            elif (row2 != None):
                artist = True
                loggedIn = True
                userID = uid
                artistSession()
            else:
                # generate the ui frame for the user
                print("invalid uid and pwd combination: try again")

        elif inp == 's': # sign up handling block
            validID = False
            uid = input("uid: ").strip()
            uid=str(uid)
            id_upper=uid.upper()
            
            c.execute('''select uid from users
                        where upper(uid)=?
                        ''',(id_upper,))
                      
            rows=c.fetchall()
                      
            if len(rows)==0:
                validID=True

            if(len(uid) < 5 and len(uid)>0 and validID==True): # sanity checks for the uid
                name = input("name: ").strip()
                pwd = input("password: ") # inserting in uid,pwd in db
                c.execute('''
                insert into users(uid,name,pwd) values(?,?,?); 
                ''', (uid, name, pwd))
                conn.commit()
                userID = uid
                loggedIn=True
                userSession()
                # generate the ui frame for the user
            print('This uid already exists or is greater than 4 characters. Try again')

        elif inp == "exit":
            exitProgram()
            return

        else:
            print("invalid command, please try again")


def startSession():
    global sessionNum, userID
    # get max session number for user and increment it
    c.execute('''
    select MAX(sno)
    from sessions
    where uid = ?
    ''', (userID,))
    maxSess = c.fetchone()

    if (maxSess[0] != None):
        maxSess = int(maxSess[0])
    else:
        maxSess = 0

    maxSess += 1

    c.execute('''
    insert into sessions(uid,sno,start) values (?,?,DATETIME('now'))
    ''', (userID, maxSess))
    sessionNum = maxSess

    print("\nListening session has started\n")
    conn.commit()


def searchKeywordSong():
    inp = input("Search a song or playlist: ")
    inp = inp.split()  # making this into list of words seperated by whitespace
    if (len(inp) == 0):
        print("invalid search")
        return
    c.execute('''
    select title,sid,duration
    from songs;
    ''')
    
    row = c.fetchall()
    length = len(row)

    A = []  # default, if A[0]=-1 then this means it is equal to null
    current = 0
    for i in range(length):
        freq = 0  # num of matches
        for j in range(len(inp)):
            keyword = str(inp[j]).upper()
            song = row[i][0]
            sid = row[i][1]
            duration = row[i][2]
            caseSong = song.upper()
            if keyword in caseSong:
                if (freq == 0):
                    A.append([song, freq+1, "song", sid, duration])
                else:
                    A[current] = [song, freq+1, "song", sid, duration]
                freq += 1
        if freq > 0:
            current += 1  # increment counter only if there is at least a match

    c.execute('''
    select title,pid
    from playlists;
    ''')
    
    row = c.fetchall()
    length = len(row)

    for i in range(length):
        title = row[i][0]
        pid = row[i][1]
        caseTitle = title.upper()
        freq = 0  # num of matches
        c.execute('''
        select SUM(s.duration)
        from plinclude pl, songs s
        where pl.pid=?
        and pl.sid=s.sid
        ''', (pid,))
        duration = c.fetchone()
        try:
            duration=duration[0]
        except:
            duration=duration
            
        if duration == None:  # handle case where playlist has no songs; i.e no duration
            duration=0
            
        for j in range(len(inp)):
            keyword = str(inp[j]).upper()
            if keyword in caseTitle:
                if freq == 0:
                    A.append([title, freq+1, "playlist", pid, duration])
                else:
                    A[current] = [title, freq+1, "playlist", pid, duration]
                freq += 1

        if freq > 0:
            current += 1  # increment counter only if there is at least a match

    try:
        A.sort(reverse=True, key=lambda x: x[1])
    except:
        print("no matches found\n")
        return
    paginateSP(A)
    return


def paginateSP(A: list): # paginate sp handles ui presentation of search results for songs/playlists
    if len(A)==0:
        print("no matches/results found\n")
        return
    num_rows = len(A)
    maxpage = num_rows//5 # find num pages
    if (num_rows % 5 != 0):
        maxpage += 1
    page = 1
    a = 0
    print("")
    for a in range(5): # print first 5 results
        if (a < len(A)):

            print(str(a) + ". " + str(A[a][2]) + ": " + str(A[a][0]
                                                            ) + ", " + str(A[a][3]) + ", " + str(A[a][4]))
    print("page: " + str(page)+"/" + str(maxpage))

    while (True):
        inp = input("""
[press 'ROWNUMBER' to select a song/playlist (i.e. 21)]
[type 'p NUMBER' to view a page(i.e. 'p 20')]
['type 'next' to view next page]
[back' to view the previous page]
[first' and 'last' for the first last pages, respectively]
[press any other button to go back to the menu]
--choose here: """)

        inp = inp.split()
        length = len(inp)
        if (length == 2 and inp[0] == 'p'): # sanity checks for input validity
            try:
                temp_page = int(inp[1])
            except:
                return
            if (temp_page <= maxpage and temp_page >0 ):
                page=temp_page
                printPage(A, page, maxpage)
        elif (length == 1):
            if (inp[0] == "next"): # next page block generation
                page += 1
                if (page <= maxpage):
                    printPage(A, page, maxpage)
                else:
                    page-=1
            elif (inp[0] == "prev"): # previous page block generation
                if (page > 1):
                    page -= 1
                    printPage(A, page, maxpage)
                else:
                    print("invalid command: this is the first page\n")
            elif (inp[0] == "first"):
                page = 1
                printPage(A, page, maxpage)

            elif (inp[0] == "last"):
                page = maxpage
                printPage(A, page, maxpage)

            else:
                try:
                    rownum = int(inp[0])
                except:
                    return
                if (rownum >= 0 and rownum < num_rows): # sanity check for index provided
                    if (A[rownum][2] == "playlist"):
                        selectPl(A[rownum][3]) # select playlist
                        return
                    else:
                        selectSong(A[rownum][3]) # select song
                        return
                return
        else:
            return


# helper functions that calculates number of matches artist song titles or artist name have with list of keywords
def artistMatches(songs: 'list[str]', keywords: 'list[str]', name: str) -> int:
    count=0
    if(len(songs)==0):
        for kw in keywords:
            if str(kw).upper() in str(name).upper():
                count += 1
        return count
            
            
    for keyword in keywords:
        for song in songs:
            if str(keyword).upper() in str(song).upper():
                count += 1
                break
            if str(keyword).upper() in str(name).upper():
                count += 1
                break
    return count


def printPageA(A: list, page: int, max: int): # helper function that prints artist search pages
    print("")
    a = (page-1)*5
    limit = a+5
    num_rows=len(A)
    while (a < limit and a < num_rows):
        print(str(a) + ". " + str(A[a][1]) + ", " + str(A[a][0]) + ", " + str(A[a][2]) +  ", "+ str(A[a][3]))
        a += 1
        
    print("--page: " + str(page) + "/"+str(max) + "\n")
    return


def paginateArtist(A: list): # paginate helper func. that enable ui presentation of artist search results
    if len(A)==0:
        print("no matches/results found\n")
        return
    num_rows = len(A)
    maxpage = num_rows//5
    if (num_rows % 5 != 0):
        maxpage += 1
    page = 1
    a = 0
    print("")
    for a in range(5):  # printing first results (max. 5)
        if a < num_rows:
            print(str(a)+". " + str(A[a][1]) + ", " +
                  str(A[a][0]) + ", " + str(A[a][2])+ ", "+str(A[a][3]))
    print("page: " + str(page)+"/" + str(maxpage))

    while (True):
        inp = input("""
[press 'ROWNUMBER' to select an artist (i.e. 21)]
[type 'p NUMBER' to view a page(i.e. 'p 20')]
['type 'next' to view next page]
[back' to view the previous page]
[first' and 'last' for the first last pages, respectively]
[press any other button to go back to the menu]
--choose here: """)        
        inp = inp.split()
        length = len(inp)
        if (length == 1):
            if (inp[0] == "next"): # next page generation
                page += 1
                if (page <= maxpage):
                    printPageA(A, page, maxpage)
                else:
                    page-=1
            elif (inp[0] == "prev"): # previous page generation
                if (page > 1):
                    page -= 1
                    printPageA(A, page, maxpage)
                else:
                    print("invalid command: this is the first page\n") # sanity checks implemented 
            elif (inp[0] == "first"):
                page = 1
                printPageA(A, page, maxpage)

            elif (inp[0] == "last"):
                page = maxpage
                printPageA(A, page, maxpage)

            else:
                try:
                    rownum = int(inp[0])
                except:
                    return
                if(rownum>=0 and rownum <num_rows): # sanity check
                    selectArtist(A[rownum][0])
                return
        elif (length == 2 and inp[0] == 'p'): # parsing and sanity check 
            try:
                temp_page = int(inp[1])
            except:
                return
            if (temp_page <= maxpage and temp_page>0):
                page=temp_page
                printPage(A, page, maxpage)
        else:
            return


def selectArtist(aid: int): # enables user to select artist and perform song actions after
    c.execute('''
    select *
    from songs s, perform p
    where p.aid=?
    and s.sid=p.sid
    ''', (aid,))
    songs = c.fetchall()
    i = 1
    print("\nSongs:") # print songs
    for song in songs:
        print(str(i) + ". " + str(song[1]) +
              ", " + str(song[0]) + ", " + str(song[2]))
        i += 1

    inp = input(
        "[type a valid rownumber (ex: 20) to select a song or any other button to return to the main menu]: ")
    inp.split()
    if (len(inp) != 1):
        return
    try:
        inp = int(inp)-1
    except:
        print("returning to menu\n")
        return
    if(inp < len(songs) and inp >= 0):
        selectSong(songs[inp][0]) # select user-selected song
    return


def keywordArtist():
    inp = input("Search an artist: ")
    inp = inp.split()  # making this into list of words seperated by whitespace
    if (len(inp) == 0):
        print("invalid search")
        return
    c.execute('''
    select a.name,a.aid,a.nationality,COUNT(p.sid)
    from artists a, perform p
    where a.aid=p.aid
    group by a.name,a.aid,a.nationality;
    '''
              )

    rows = c.fetchall()
    A = []  # means empty array i.e. no matches
    for row in rows:
        name = row[0]
        aid = row[1]
        c.execute('''
        select s.title
        from songs s, perform p 
        where p.aid=?
        and p.sid=s.sid;
        ''', (aid,))
        songs = c.fetchall()
        num_matches = artistMatches(songs, inp, name)
        if num_matches > 0:
            A.append([row[1], row[0], row[2],row[3], num_matches])
    try:
        A.sort(reverse=True, key=lambda x: x[4])
    except:
        print("no matches found\n")
        return

    paginateArtist(A)
    return


def selectSong(sid: int): # select song enables user to select and perform actions on song from the ui 
    while (True):
        inp = input("[type 'info' for more information about the song]\n['add' to add it to a playlist or 'listen' to listen to it]\n[press any button to return to menu]\npress here: ")
        
        if inp == "": # parsing block to determine function call
            return
        inp = str(inp)
        if inp == 'info':
            songInfo(sid)
            return
        elif inp == 'add':
            addToPl(sid)
            return
        elif inp == 'listen':
            listenSong(sid)
            return
        elif inp == 'exit':
            exitProgram()

        else:
            return


def printPage(A: list, page: int, max: int): # helper function to print user-selected search page
    print("")
    a = (page-1)*5
    limit = a+5
    num_rows=len(A)
    while (a < limit and a < num_rows):
        print(str(a) + ". " + str(A[a][0]) + ", " + str(A[a][2]) + ", " + str(A[a][3]) + ", " + str(A[a][4]))
        a += 1
    print("--page: " + str(page)+ '/' + str(max)+"\n")    
    return



def selectPl(pid: int): # enables user to select pl and perform actions on songs in it 
    c.execute('''
    select s.sid,s.title,s.duration
    from songs s, plinclude p
    where p.pid=?
    and p.sid=s.sid;
    ''', (pid,))
    A = c.fetchall()
    i = 0
    print("\n--Songs in Playlist") # printing pl songs
    for row in A:
        print(str(i) + ". " + str(row[1]) + ", " +
              str(row[0]) + ", " + str(row[2]))
        i += 1

    inp = input(
        "type 'ROWNUMBER' (i.e. 3) to select song, press any other button to return to the main menu: ")
    try:
        row = int(inp.strip())
    except:
        return

    if (row >= 0 and row < len(A)):
        selectSong(A[row][0])
        return
    return


def listenSong(sid: int): # enables user to listen to a song, this action is reflected in the db 
    if (sessionNum == -1):
        startSession()
    # locate any active sessions
    c.execute('''
    select sid 
    from listen
    where sno= ?
    and sid = ?;
    ''', (sessionNum, sid))
    if c.fetchone() != None: # update session count
        c.execute('''
        update listen
        set cnt = cnt+1
        where sno = ?
        and sid = ?;
        ''', (sessionNum, sid))
    else:
        c.execute('''
        insert into listen(uid,sid,sno,cnt) values(?,?,?,1);
        ''', (userID, sid, sessionNum))
    print("\nListened to song successfully!\n")
    conn.commit()
    return


def songInfo(sid: int): # printing song info 
    performers = [""]
    c.execute('''
    select * 
    from songs
    where sid=?;
    ''', (sid,))
    songRow = c.fetchone()
    print("\nBasic Info\n[sid, title, duration]: " +str(songRow[0]) + ", " + str(songRow[1]) + ", " + str(songRow[2]) + '\n')
    print("Performers:") # print performers 
    c.execute('''
        select a.name
        from artists a, perform p
        where p.sid=?
        and p.aid=a.aid;
        ''', (sid,))
    performers = c.fetchall()
    if len(performers)==0:
        print("None")
    else:
        for performer in performers:
            print(', '.join(performer))
    

    print("\nPlaylists:") # print playlists it is in
    c.execute('''
        select p.title
        from plinclude pl, playlists p
        where pl.sid=?
        and pl.pid=p.pid;
        ''', (sid,))

    playlists = c.fetchall()
    
    if len(playlists)==0:
        print("The song is in no playlist\n")
        return
    for playlist in playlists:
        print(', '.join(playlist))



def addToPl(sid: int): # adds a user selected song to a playlist
    c.execute('''
    select title,pid
    from playlists
    where uid=?;
    ''', (userID,))
    pl = c.fetchall()
    inp=input("press 'y' to add to existing playlist, 'n' to add it to a new one: ") # prompt user to add to existing or new pl
    if len(pl)>0 and inp=='y':
        for i in range(len(pl)):
            print(str(i) + ". " + str(pl[i][0]) + ", pid: " + str(pl[i][1]))
        inp = input(
            "select a playlist to add the song to (using index number): ")
        try: # sanity check
            inp = int(inp)
            if(inp<0):
                print("invalid index (negative)")
                return
            playlist = pl[inp]
        except:
            print("invalid input: index does not exist or wrong type of input\n")
            return
        c.execute('''
        select MAX(sorder)
        from plinclude
        where pid=?;
        ''', (playlist[1],))
        order = c.fetchone()
        if order==None:
            order=1
        else:
            order=order[0]+1

        c.execute('''
        select sid
        from plinclude
        where sid=?
        and pid=?;
        ''',(sid,playlist[1]))
        if c.fetchone()!=None: # making sure song is not already in playlist
            print("\nThis song is already in the playlist")
            return
        
        c.execute('''
        insert into plinclude(pid,sid,sorder) values(?,?,?);
        ''', (playlist[1], sid, order))
        

    elif((inp=='y' and len(pl)==0) or inp=='n'):
        inp = input(
            "Type the name of the new playlist the song will be added to: ")
        inp = str(inp)
        inp=inp.strip()
        c.execute('''  
        select MAX(pid)
        from playlists;
        ''')

        pid = c.fetchone()  # increment max pid in table to obtain new pid for the new playlist
        if pid == None:
            pid = -1
        else:
            pid=pid[0]
            
        pid+=1

        # insert song in relevant database tables
        c.execute('''
        insert into playlists(pid,title,uid) values(?,?,?); 
        ''', (pid, inp, userID))
        
        c.execute('''
        insert into plinclude(pid,sid,sorder) values(?,?,1);
        ''', (pid, sid))
        print("succesfully added song to playlist\n")
    else:
        print("invalid command\n")
    print("song added successfully to playlist!")
    conn.commit()
    return


def addSong(title: str, duration: int):
    c.execute(  # checking if artist has a song with same title and duration
        '''
        select s.sid
        from perform p, songs s
        where p.aid=?
        and p.sid=s.sid
        and upper(s.title)=?
        and s.duration=?;
        ''', (userID, title.upper(), duration))
    result = c.fetchone()

    if result != None: # making sure song does not exist
        inp = input(
            "a song with the same title and duration exists: press 'y' to continue, press any other key to cancel: ")
        inp=str(inp)
        if inp != 'y':
            return
        
    # calculate new song sid 
    c.execute(
        '''
        select MAX(sid)
        from songs;
        '''
    )
    new_id = c.fetchone()
    if (new_id[0] == None):
        new_id = 0
    else:
        new_id=new_id[0]+1
        

    c.execute(
        '''
        insert into songs(sid,title,duration) values(?,?,?); 
        ''', (new_id, title, duration)
    )

    c.execute(
        '''
        insert into perform(aid,sid) values(?,?); 
        ''', (userID, new_id)
    )

    addPerformer(new_id)
    conn.commit()
    return


def addPerformer(sid: int):
    inp=input("Would you like to add a performer?\n Press 'y' or 'n': ")
    inp.strip()
    if inp=='n':
        return
    true = 1
    while (true):
        inp = input("type artist aid to add: ")
        inp = int(inp)
        c.execute(
            '''
            insert into perform(aid,sid) values(?,?); 
            ''', (inp, sid)
        )
        inp = input(
            "press 1 to add another artist, press any other button if done: ")
        try:
            true = int(inp)
        except:
            return
    conn.commit()
    return


def topFansPl(): # gets top fans and playlists of artist
    c.execute(  
        '''
        select u.name,u.uid, SUM(s.duration*l.cnt)
        from users u, listen l,perform p, songs s
        where l.sid=p.sid
        and p.aid=?
        and l.sid=s.sid
        group by u.uid,u.name
        ORDER BY SUM(s.duration*l.cnt) DESC
        LIMIT 3;
        ''', (userID,))

    fans = c.fetchall()
    print("\nTop Fans:")
    if (len(fans)>0):
        for row in fans:
            print(row[0]+", "+row[1])
    else:
        print("No fans\n")
        
    c.execute(  
        '''
        select pl.title,pl.pid, COUNT(p.sid) AS cnt
        from plinclude pli, playlists pl,perform p
        where pli.sid=p.sid
        and p.aid=?
        and pli.pid=pl.pid
        group by pl.title,pl.pid
        order by cnt
        LIMIT 3;
        ''', (userID,))
    playlists = c.fetchall()
    print("Top Playlists:")
    if (len(playlists) > 0):
        for row in playlists:
            print(str(row[0])+", "+str(row[1]))
    else:
        print("Your songs aren't in any playlist\n")
    return 


def exitProgram(): # end session and end program 
    endSession()
    conn.commit()
    exit()


def endSession():
    global sessionNum
    """
    closes specified session in database by assigning it an end time set to now
    :param str uid: uid of session
    :param int sno: sno of session
    :param sqlite3.Connection connection: connection to database being searched
    :return: none
    """

    c.execute("""
        UPDATE sessions
        SET end = DATETIME('now')
        WHERE uid = ? AND sno = ?;
    """, (userID, sessionNum))
    sessionNum = -1
    print("\n Any active listening session has now ended\n")
    conn.commit()


# start menu loop
def main():
    if conn != None:
        login()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
