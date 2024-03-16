# generates random playlists in an easy to parse format, then prints it to console
# script written by James Laidlaw


import random

users = []
for i in range(1, 21):
    users.append(str(i))

songs = []
for i in range(1, 13):
    songs.append(str(i))

nameBase = "playlist"

playlistMakers = random.sample(users, 10)


class playlist:
    pid: int
    title: str
    uid: str

    def __init__(self, pid, title, uid) -> None:
        self.pid = pid
        self.title = title
        self.uid = uid


# make 10 random playlists
playlists: 'list[playlist]' = []
for i, user in enumerate(playlistMakers):
    playlists.append(playlist(i, nameBase + str(i), user))


class playlistAssign:
    pid: int
    sid: int
    sorder: int

    def __init__(self, pid, sid, sorder) -> None:
        self.pid = pid
        self.sid = sid
        self.sorder = sorder


# for each playlist, add 1-10 random songs
playlistAssignments: "list[playlistAssign]" = []
for playlistEntity in playlists:
    songcount = random.randint(1, 10)
    songlist = random.sample(songs, songcount)
    for i, song in enumerate(songlist):
        playlistAssignments.append(playlistAssign(playlistEntity.pid, song, i))

# print playlists
#pid, title, uid
print("[")
for playlistEntity in playlists:
    print("['{}', '{}', '{}' ],".format(playlistEntity.pid,
          playlistEntity.title, playlistEntity.uid))
print("]")
print("\n \n \n")

# print song playlist assignments
#pid, sid, sorder
print("[")
for playlistAssignment in playlistAssignments:
    print("['{}', '{}', '{}' ],".format(playlistAssignment.pid,
          playlistAssignment.sid, playlistAssignment.sorder))
print("]")
