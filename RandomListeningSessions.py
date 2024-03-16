# generates random listening sessions in an easy to parse format, then prints it to console
# script written by James Laidlaw


import time
import random


nextUserSno = {}
for i in range(1, 21):
    nextUserSno[str(i)] = 0

users = []
for i in range(1, 21):
    users.append(str(i))

songs = []
for i in range(1, 13):
    songs.append(str(i))


# generate some listening sessions


class listeningSession:
    startTime: str
    endTime: str
    uid: str
    sno: int

    def __init__(self) -> None:
        now = time.time()
        start = now - random.randint(1000, 100000)
        end = start + random.randint(0, 990)
        startTimeRaw = time.gmtime(start)
        endTimeRaw = time.gmtime(end)
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S", startTimeRaw)
        self.endTime = time.strftime("%Y-%m-%d %H:%M:%S", endTimeRaw)
        self.uid = random.choice(users)
        self.sno = nextUserSno[self.uid]
        nextUserSno[self.uid] = nextUserSno[self.uid] + 1


# generate 30 listening sessions
listeningSessions: 'list[listeningSession]' = []
for i in range(30):
    listeningSessions.append(listeningSession())


class songListen:
    uid: str
    sno: int
    sid: int
    cnt: int

    def __init__(self, session: listeningSession, sid: int, cnt: int) -> None:
        self.uid = session.uid
        self.sno = session.sno
        self.sid = sid
        self.cnt = cnt


songListens: 'list[songListen]' = []
# for each listening session, generate 1-5 listens of unique songs
for session in listeningSessions:
    songCount = random.randint(1, 5)
    listenedSongs = random.sample(songs, songCount)
    for song in listenedSongs:
        songListens.append(songListen(session, song, random.randint(1, 10)))


# print listening sessions in usable format
#uid, sno, start, end
print("[")
for session in listeningSessions:
    print("['{}', '{}', '{}', '{}'],".format(session.uid,
          session.sno, session.startTime, session.endTime))
print("]")
print("\n \n \n")


# print song listens
#uid, sno, sid, cnt
print("[")
for listen in songListens:
    print("['{}', '{}', '{}', '{}'],".format(
        listen.uid, listen.sno, listen.sid, listen.cnt))
print("]")
