# resets the test.db database and repopulates it with ~20 entries in each table
# script written by James Laidlaw
import sqlite3
tableGenFile = open("prj-tables.sql", "r")
tableGenScript = tableGenFile.read()
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.executescript(tableGenScript)
conn.commit()

# sid, song title, song duration, aid, artist name, artist nationality, artist password
artistSongInfo = [
    ["1",	"Blinding Lights",	"200",	"1",	"The Weeknd",	"Canadian",	"ArtistPassword1"],
    ["2",	"Out of Time",	"233",	"1",	"The Weeknd",	"Canadian",	"ArtistPassword1"],
    ["3",	"Gasoline",	"293",	"1",	"The Weeknd",	"Canadian",	"ArtistPassword1"],
    ["4",	"The Twist",	"261",	"2",	"Chubby Checker",	"American",	"ArtistPassword2"],
    ["5",	"Smooth",	"150",	"3",	"Santana",	"American",	"ArtistPassword3"],
    ["5",	"Smooth",	"150",	"4",	"Rob Thomas",	"American",	"ArtistPassword4"],
    ["6",	"Mack the Knife",	"198",	"5",	"Bobby Darin",	"American",	"ArtistPassword5"],
    ["7",	"Uptown Funk",	"164",	"6",	"Mark Ronson",	"British",	"ArtistPassword6"],
    ["7",	"Uptown Funk",	"164",	"7",	"Bruno Mars",	"American",	"ArtistPassword7"],
    ["8",	"How Do I Live",	"289",	"8",	"LeAnn Rimes",	"American",	"ArtistPassword8"],
    ["9",	"Party Rock Anthem",	"232",	"9",	"LMFAO",	"American",	"ArtistPassword9"],
    ["9",	"Party Rock Anthem",	"232",	"10",
        "Lauren Bennett",	"English",	"ArtistPassword10"],
    ["9",	"Party Rock Anthem",	"232",	"11",
        "GoonRock",	"American",	"ArtistPassword11"],
    ["10",	"I Gotta Feeling",	"199",	"12",
        "The Black Eyed Peas",	"American",	"ArtistPassword12"],
    ["11",	"Macarena",	"264",	"13",	"Los Del Rio",	"Spanish",	"ArtistPassword13"],
    ["12",	"Shape of You",	"277",	"14",	"Ed Sheeran",	"English",	"ArtistPassword14"],
    ["13", "Baby", "210", "aau", "Justin Beiber", "Canadian", "aau"]
]
# add artists
prevAID = '-1'
for artist in artistSongInfo:
    if (prevAID != artist[3]):
        cursor.execute("INSERT INTO artists VALUES ('{}','{}','{}','{}')".format(
            artist[3], artist[4], artist[5], artist[6]))
        conn.commit()
    prevAID = artist[3]

# add songs
prevSID = '-1'
for song in artistSongInfo:
    if (prevSID != song[0]):
        cursor.execute("INSERT INTO songs VALUES ({},'{}','{}')".format(
            song[0], song[1], song[2]))
        conn.commit()
    prevSID = song[0]

# add performed relation
for songArtist in artistSongInfo:
    cursor.execute("INSERT INTO perform VALUES ('{}',{})".format(
        songArtist[3], songArtist[0]))
    conn.commit()


#uid, name, password
userInfo = [
    ["1",	"Liam",	"UserPassword1"],
    ["2",	"Noah",	"UserPassword2"],
    ["3",	"Oliver",	"UserPassword3"],
    ["4",	"Elijah",	"UserPassword4"],
    ["5",	"James",	"UserPassword5"],
    ["6",	"William",	"UserPassword6"],
    ["7",	"Benjamin",	"UserPassword7"],
    ["8",	"Lucas",	"UserPassword8"],
    ["9",	"Henry",	"UserPassword9"],
    ["10",	"Theodore",	"UserPassword10"],
    ["11",	"Olivia",	"UserPassword11"],
    ["12",	"Emma",	"UserPassword12"],
    ["13",	"Charlotte",	"UserPassword13"],
    ["14",	"Amelia",	"UserPassword14"],
    ["15",	"Ava",	"UserPassword15"],
    ["16",	"Sophia",	"UserPassword16"],
    ["17",	"Isabella",	"UserPassword17"],
    ["18",	"Mia",	"UserPassword18"],
    ["19",	"Evelyn",	"UserPassword19"],
    ["20",	"Harper",	"UserPassword20"],
    ["aau", "Justin Beiber", "aau"]
]

# add users
for user in userInfo:
    cursor.execute("INSERT INTO users VALUES ('{}','{}','{}')".format(
        user[0], user[1], user[2]))
    conn.commit()

#uid, sno, start, end
sessionInfo = [
    ['18', '0', '2022-10-26 13:22:15', '2022-10-26 13:38:01'],
    ['8', '0', '2022-10-26 10:29:20', '2022-10-26 10:36:39'],
    ['11', '0', '2022-10-26 16:27:23', '2022-10-26 16:32:51'],
    ['4', '0', '2022-10-25 18:57:38', '2022-10-25 18:58:34'],
    ['11', '1', '2022-10-25 18:10:11', '2022-10-25 18:14:14'],
    ['19', '0', '2022-10-26 19:22:52', '2022-10-26 19:31:26'],
    ['1', '0', '2022-10-26 06:10:54', '2022-10-26 06:17:00'],
    ['11', '2', '2022-10-26 04:34:12', '2022-10-26 04:34:24'],
    ['10', '0', '2022-10-26 00:54:11', '2022-10-26 01:06:51'],
    ['2', '0', '2022-10-26 00:46:21', '2022-10-26 00:50:11'],
    ['12', '0', '2022-10-26 01:38:10', '2022-10-26 01:51:34'],
    ['1', '1', '2022-10-26 17:38:22', '2022-10-26 17:38:24'],
    ['13', '0', '2022-10-26 20:49:55', '2022-10-26 21:03:32'],
    ['16', '0', '2022-10-25 23:52:03', '2022-10-26 00:04:11'],
    ['4', '1', '2022-10-26 21:11:34', '2022-10-26 21:15:35'],
    ['2', '1', '2022-10-25 23:25:35', '2022-10-25 23:41:34'],
    ['18', '1', '2022-10-26 13:24:30', '2022-10-26 13:33:14'],
    ['13', '1', '2022-10-26 08:19:43', '2022-10-26 08:26:26'],
    ['1', '2', '2022-10-26 00:02:22', '2022-10-26 00:08:04'],
    ['6', '0', '2022-10-25 18:31:56', '2022-10-25 18:45:42'],
    ['8', '1', '2022-10-25 18:51:42', '2022-10-25 19:07:31'],
    ['8', '2', '2022-10-25 21:35:43', '2022-10-25 21:46:21'],
    ['19', '1', '2022-10-26 18:12:41', '2022-10-26 18:21:50'],
    ['16', '1', '2022-10-26 02:11:17', '2022-10-26 02:11:40'],
    ['13', '2', '2022-10-26 09:12:26', '2022-10-26 09:24:28'],
    ['8', '3', '2022-10-25 20:42:42', '2022-10-25 20:44:24'],
    ['5', '0', '2022-10-26 20:26:52', '2022-10-26 20:34:15'],
    ['11', '3', '2022-10-26 13:52:53', '2022-10-26 14:03:47'],
    ['19', '2', '2022-10-26 00:41:28', '2022-10-26 00:54:55'],
    ['4', '2', '2022-10-26 14:20:48', '2022-10-26 14:23:05']
]

# add listening sessions
for session in sessionInfo:
    cursor.execute("INSERT INTO sessions VALUES ('{}',{},'{}', '{}')".format(
        session[0], session[1], session[2], session[3]))
    conn.commit()

#uid, sno, sid, cnt
listenInfo = [
    ['18', '0', '3', '1'],
    ['8', '0', '7', '2'],
    ['8', '0', '4', '9'],
    ['8', '0', '6', '4'],
    ['8', '0', '2', '4'],
    ['8', '0', '5', '6'],
    ['11', '0', '9', '4'],
    ['11', '0', '1', '3'],
    ['11', '0', '4', '1'],
    ['11', '0', '7', '5'],
    ['11', '0', '5', '2'],
    ['4', '0', '7', '1'],
    ['11', '1', '2', '9'],
    ['19', '0', '10', '6'],
    ['19', '0', '2', '9'],
    ['19', '0', '8', '5'],
    ['19', '0', '11', '4'],
    ['1', '0', '2', '10'],
    ['11', '2', '3', '9'],
    ['11', '2', '4', '5'],
    ['10', '0', '7', '8'],
    ['10', '0', '11', '9'],
    ['10', '0', '9', '7'],
    ['10', '0', '10', '2'],
    ['2', '0', '7', '8'],
    ['12', '0', '12', '9'],
    ['12', '0', '3', '7'],
    ['1', '1', '3', '3'],
    ['1', '1', '8', '2'],
    ['1', '1', '9', '2'],
    ['13', '0', '10', '9'],
    ['13', '0', '2', '9'],
    ['13', '0', '7', '5'],
    ['16', '0', '1', '10'],
    ['4', '1', '2', '10'],
    ['4', '1', '10', '6'],
    ['2', '1', '8', '5'],
    ['2', '1', '3', '6'],
    ['18', '1', '6', '6'],
    ['18', '1', '1', '1'],
    ['18', '1', '3', '9'],
    ['18', '1', '9', '3'],
    ['18', '1', '7', '10'],
    ['13', '1', '8', '4'],
    ['13', '1', '12', '1'],
    ['13', '1', '2', '5'],
    ['13', '1', '9', '7'],
    ['13', '1', '3', '10'],
    ['1', '2', '7', '8'],
    ['1', '2', '2', '2'],
    ['1', '2', '4', '10'],
    ['1', '2', '10', '5'],
    ['6', '0', '11', '2'],
    ['6', '0', '6', '2'],
    ['6', '0', '12', '10'],
    ['8', '1', '4', '10'],
    ['8', '2', '6', '5'],
    ['8', '2', '11', '7'],
    ['19', '1', '5', '7'],
    ['19', '1', '6', '6'],
    ['16', '1', '9', '4'],
    ['16', '1', '6', '5'],
    ['16', '1', '11', '4'],
    ['16', '1', '5', '3'],
    ['13', '2', '9', '6'],
    ['8', '3', '3', '4'],
    ['8', '3', '10', '7'],
    ['8', '3', '9', '5'],
    ['8', '3', '6', '7'],
    ['8', '3', '12', '7'],
    ['5', '0', '2', '6'],
    ['5', '0', '1', '4'],
    ['5', '0', '4', '2'],
    ['11', '3', '5', '10'],
    ['11', '3', '10', '9'],
    ['11', '3', '7', '6'],
    ['11', '3', '4', '9'],
    ['11', '3', '9', '3'],
    ['19', '2', '1', '7'],
    ['4', '2', '3', '2'],
    ['4', '2', '8', '10'],
    ['4', '2', '11', '9'],
    ['4', '2', '7', '10'],
    ['4', '2', '9', '8']
]

# add song listens
for listen in listenInfo:
    cursor.execute("INSERT INTO listen VALUES ('{}',{},{}, {})".format(
        listen[0], listen[1], listen[2], listen[3]))
    conn.commit()

playlistInfo = [
    ['0', 'playlist0', '5'],
    ['1', 'playlist1', '14'],
    ['2', 'playlist2', '9'],
    ['3', 'playlist3', '8'],
    ['4', 'playlist4', '18'],
    ['5', 'playlist5', '6'],
    ['6', 'playlist6', '20'],
    ['7', 'playlist7', '3'],
    ['8', 'playlist8', '2'],
    ['9', 'playlist9', '13'],
]

# add playlists
for playlist in playlistInfo:
    cursor.execute("INSERT INTO playlists VALUES ({},'{}','{}')".format(
        playlist[0], playlist[1], playlist[2]))
    conn.commit()


playlistItemInfo = [
    ['0', '12', '0'],
    ['0', '7', '1'],
    ['0', '8', '2'],
    ['0', '5', '3'],
    ['0', '11', '4'],
    ['0', '4', '5'],
    ['0', '10', '6'],
    ['0', '1', '7'],
    ['1', '4', '0'],
    ['1', '12', '1'],
    ['1', '9', '2'],
    ['1', '10', '3'],
    ['1', '1', '4'],
    ['1', '8', '5'],
    ['2', '6', '0'],
    ['3', '6', '0'],
    ['3', '12', '1'],
    ['3', '3', '2'],
    ['3', '5', '3'],
    ['3', '4', '4'],
    ['3', '10', '5'],
    ['3', '9', '6'],
    ['3', '8', '7'],
    ['3', '7', '8'],
    ['3', '11', '9'],
    ['4', '6', '0'],
    ['4', '1', '1'],
    ['4', '9', '2'],
    ['4', '11', '3'],
    ['4', '12', '4'],
    ['4', '4', '5'],
    ['4', '2', '6'],
    ['4', '10', '7'],
    ['4', '8', '8'],
    ['4', '5', '9'],
    ['5', '4', '0'],
    ['5', '11', '1'],
    ['5', '9', '2'],
    ['5', '7', '3'],
    ['5', '6', '4'],
    ['5', '10', '5'],
    ['5', '3', '6'],
    ['5', '2', '7'],
    ['6', '9', '0'],
    ['6', '3', '1'],
    ['6', '4', '2'],
    ['7', '5', '0'],
    ['7', '9', '1'],
    ['7', '7', '2'],
    ['7', '8', '3'],
    ['7', '4', '4'],
    ['7', '6', '5'],
    ['7', '3', '6'],
    ['7', '1', '7'],
    ['7', '2', '8'],
    ['7', '10', '9'],
    ['8', '7', '0'],
    ['9', '6', '0'],
    ['9', '2', '1'],
    ['9', '9', '2'],
]

# add playlist song assignments
for playlistAssignment in playlistItemInfo:
    cursor.execute("INSERT INTO plinclude VALUES ({},{},{})".format(
        playlistAssignment[0], playlistAssignment[1], playlistAssignment[2]))
    conn.commit()
