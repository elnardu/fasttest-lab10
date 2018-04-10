#!/usr/bin/python3

import multiprocessing
import subprocess
import random
import socket
import difflib
import os
import sys

CURRENTDIR = os.path.dirname(os.path.realpath(__file__))

def getRandomPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        port = random.randint(1, 65535)
        try:
            s.bind(("127.0.0.1", port)) # test if port is in use
        except socket.error:
            continue
        
        s.close()
        return port


def runTest(testNum, q, orgOutput):
    port = getRandomPort()
    try:
        testPs = subprocess.Popen("{}/test-server{}.sh ./ServerIRC {}".format(CURRENTDIR, testNum, port),
                           shell=True, stdout=subprocess.PIPE)
    except Exception as e:
        print("Cannot start new process")
        print(e)
        q.put((testNum, False, 'TEST RUN FAILED'))
        sys.exit(1)
        return

    testPs.wait()

    print("TEST {} DONE".format(testNum))

    output = testPs.stdout.read().decode('utf-8').splitlines()
    orgOutput = orgOutput.splitlines()

    if output == orgOutput:
        q.put((testNum, True))
        return

    d = difflib.Differ()
    diff = d.compare(output, orgOutput)
    q.put((testNum, False, '\n'.join(diff)))    


def printResults(results):
    for t in range(1, 11):
        if results[t][0]:
            print("--- TEST {} PASSED ---".format(t))
        else:
            print("--- TEST {} FAILED ---".format(t))
            print(results[t][1])
    
    print("-----------------")
    for t in range(1, 11):
        if results[t][0]:
            print("TEST {} PASSED".format(t))
        else:
            print("TEST {} FAILED".format(t))
    print("-----------------")



def main():
    pool = []
    results = {}
    print(CURRENTDIR)
    print("Good Luck")
    if subprocess.call("make", shell=True):
        print("MAKE FAILED")
        return 1
    
    # to prevent test-server scripts from killing our processes
    subprocess.call("rm ./ServerIRC", shell=True)
    subprocess.call("cp ./IRCServer ./ServerIRC", shell=True)

    for t in range(1, 11):
        q = multiprocessing.Queue()
        t = multiprocessing.Process(target=runTest, args=(t, q, ORGOUTPUT[t-1]))
        t.start()
        pool.append((t, q))
    
    for t, q in pool:
        t.join()
        res = q.get()
        results[res[0]] = res[1:]

    printResults(results)

    subprocess.call(
        "kill -9 `ps | grep ServerIRC | awk '{ print $1;}'`", shell=True)
    


# Output of the original program

ORGOUTPUT = [
    """Start Test 1
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Print Users
GET-ALL-USERS superman clarkkent
response:
aquaman
mary
spiderman
superman


Killing Server
""",
    """Start Test 2
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent java-programming
response:
OK

ENTER-ROOM aquaman xyz java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM superman clarkkent java-programming
response:
aquaman
superman


Killing Server
""",
    """Start Test 3
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent java-programming
response:
OK

ENTER-ROOM aquaman xyz java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM superman clarkkent java-programming
response:
aquaman
superman


Enter another user
ENTER-ROOM mary poppins java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM mary poppins java-programming
response:
aquaman
mary
superman


Killing Server
""",
    """Start Test 4
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent java-programming
response:
OK

ENTER-ROOM aquaman xyz java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM superman clarkkent java-programming
response:
aquaman
superman


Enter another user
ENTER-ROOM mary poppins java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM mary poppins java-programming
response:
aquaman
mary
superman


Leave room
LEAVE-ROOM aquaman xyz java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM mary poppins java-programming
response:
mary
superman


Leave room
LEAVE-ROOM spiderman peterpark java-programming
response:
ERROR (No user in room)

Print users in room
GET-USERS-IN-ROOM mary poppins java-programming
response:
mary
superman


Killing Server
""",
    """Start Test 5
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent java-programming
response:
OK

ENTER-ROOM aquaman xyz java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM superman clarkkent java-programming
response:
aquaman
superman


Enter another user
ENTER-ROOM mary poppins java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM mary poppins java-programming
response:
aquaman
mary
superman


Send message
SEND-MESSAGE mary poppins java-programming Hi everybody!
response:
OK

SEND-MESSAGE mary poppins java-programming Welcome to the talk program!
response:
OK

Get messages
GET-MESSAGES superman clarkkent 0 java-programming
response:
1 mary Welcome to the talk program!


Killing Server
""",
    """Start Test 6
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent java-programming
response:
OK

ENTER-ROOM aquaman xyz java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM superman clarkkent java-programming
response:
aquaman
superman


Enter another user
ENTER-ROOM mary poppins java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM mary poppins java-programming
response:
aquaman
mary
superman


Send message
SEND-MESSAGE mary poppins java-programming Hi everybody!
response:
OK

SEND-MESSAGE mary poppins java-programming Welcome to the talk program!
response:
OK

Get messages
GET-MESSAGES superman clarkkent 0 java-programming
response:
1 mary Welcome to the talk program!


Send message
SEND-MESSAGE superman clarkkent java-programming Hi Mary!
response:
OK

SEND-MESSAGE superman clarkkent java-programming Here I am working on cs240
response:
OK

SEND-MESSAGE superman clarkkent java-programming I am testing the project
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 1
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 2
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 3
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 4
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 5
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 6
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 7
response:
OK

SEND-MESSAGE superman clarkkent java-programming message 8
response:
OK

Get messages from 0
GET-MESSAGES mary poppins 0 java-programming
response:
1 mary Welcome to the talk program!
2 superman Hi Mary!
3 superman Here I am working on cs240
4 superman I am testing the project
5 superman message 1
6 superman message 2
7 superman message 3
8 superman message 4
9 superman message 5
10 superman message 6
11 superman message 7
12 superman message 8


Enter another user
LEAVE-ROOM mary poppins java-programming
response:
OK

Get messages from 2
GET-MESSAGES superman clarkkent 2 java-programming
response:
3 superman Here I am working on cs240
4 superman I am testing the project
5 superman message 1
6 superman message 2
7 superman message 3
8 superman message 4
9 superman message 5
10 superman message 6
11 superman message 7
12 superman message 8


Killing Server
""",
    """Start Test 7
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

GET-ALL-USERS superman clarkkent
response:
aquaman
mary
spiderman
superman


Test password in GET_ALL_USERS
GET-ALL-USERS superman badpassword
response:
ERROR (Wrong password)

GET-ALL-USERS baduser badpassword
response:
ERROR (Wrong password)

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Test password in ENTER-ROOM
ENTER-ROOM superman badpassword java-programming
response:
ERROR (Wrong password)

ENTER-ROOM baduser badpassword java-programming
response:
ERROR (Wrong password)

Test password in GET-USERS-IN-ROOM
GET-USERS-IN-ROOM superman badpassword java-programming
response:
ERROR (Wrong password)

GET-USERS-IN-ROOM baduser badpassword java-programming
response:
ERROR (Wrong password)

Test password in LEAVE-ROOM
LEAVE-ROOM superman badpassword java-programming
response:
ERROR (Wrong password)

LEAVE-ROOM baduser badpassword java-programming
response:
ERROR (Wrong password)

Test password in SEND-MESSAGE
SEND-MESSAGE superman badpassword java-programming
response:
ERROR (Wrong password)

SEND-MESSAGE baduser badpassword java-programming
response:
ERROR (Wrong password)

Test password in GET-MESSAGES
GET-MESSAGES superman badpassword java-programming
response:
ERROR (Wrong password)

GET-MESSAGES baduser badpassword java-programming
response:
ERROR (Wrong password)

Test password OK
GET-ALL-USERS mary poppins
response:
aquaman
mary
spiderman
superman


Killing Server
""",
    """Start Test 8
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent java-programming
response:
OK

ENTER-ROOM aquaman xyz java-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM mary poppins java-programming
response:
aquaman
superman


Enter another user
ENTER-ROOM mary poppins java-programming
response:
OK

Send message
SEND-MESSAGE spiderman peterpark java-programming
response:
ERROR (user not in room)

Get messages
GET-MESSAGES spiderman peterpark 0 java-programming
response:
ERROR (User not in room)

Killing Server
""",
    """Start Test 9
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER aquaman xyz
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Create Room
CREATE-ROOM spiderman peterpark c-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent java-programming
response:
OK

ENTER-ROOM aquaman xyz java-programming
response:
OK

ENTER-ROOM spiderman peterpark c-programming
response:
OK

ENTER-ROOM aquaman xyz c-programming
response:
OK

ENTER-ROOM mary poppins c-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM superman clarkkent java-programming
response:
aquaman
superman


GET-USERS-IN-ROOM mary poppins c-programming
response:
aquaman
mary
spiderman


Enter another user
ENTER-ROOM spiderman peterpark c-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM spiderman peterpark c-programming
response:
aquaman
mary
spiderman


Send message
SEND-MESSAGE mary poppins c-programming Hi everybody!
response:
OK

SEND-MESSAGE mary poppins c-programming Welcome to the talk program!
response:
OK

Send message
SEND-MESSAGE superman clarkkent java-programming Welcome to java-programming!
response:
OK

SEND-MESSAGE aquaman xyz java-programming Java is based on C++!
response:
OK

Get messages
GET-MESSAGES superman clarkkent 0 java-programming
response:
1 aquaman Java is based on C++!


Get messages
GET-MESSAGES mary poppins 0 c-programming
response:
1 mary Welcome to the talk program!


Send message
SEND-MESSAGE spiderman peterpark c-programming Hi Mary!
response:
OK

SEND-MESSAGE spiderman peterpark c-programming Here I am working on cs240
response:
OK

Get messages from 0
GET-MESSAGES mary poppins 0 c-programming
response:
1 mary Welcome to the talk program!
2 spiderman Hi Mary!
3 spiderman Here I am working on cs240


LEAVE-ROOM mary poppins c-programming
response:
OK

Get messages from 2
GET-MESSAGES superman clarkkent 2 java-programming
response:
NO-NEW-MESSAGES

Killing Server
""",
    """Start Test 10
Add Users
ADD-USER superman clarkkent
response:
OK

ADD-USER spiderman peterpark
response:
OK

ADD-USER mary poppins
response:
OK

Create Room
CREATE-ROOM superman clarkkent java-programming
response:
OK

Create Room
CREATE-ROOM spiderman peterpark c-programming
response:
OK

Enter room
ENTER-ROOM superman clarkkent python-programming
response:
ERROR (No room)

ENTER-ROOM aquaman xyz python-programming
response:
ERROR (Wrong password)

ENTER-ROOM spiderman peterpark c-programming
response:
OK

ENTER-ROOM aquaman xyz c-programming
response:
ERROR (Wrong password)

ENTER-ROOM mary poppins c-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM unknown clarkkent java-programming
response:
ERROR (Wrong password)

GET-USERS-IN-ROOM mary poppins java-programming
response:


Enter another user
ENTER-ROOM spiderman peterpark c-programming
response:
OK

Print users in room
GET-USERS-IN-ROOM unknown peterpark c-programming
response:
ERROR (Wrong password)

Send message
SEND-MESSAGE superman clarkkent c-programming Hi everybody!
response:
ERROR (user not in room)

SEND-MESSAGE unknown poppins c-programming Welcome to the talk program!
response:
ERROR (Wrong password)

Send message
SEND-MESSAGE superman clarkkent java-programming Welcome to java-programming!
response:
ERROR (user not in room)

SEND-MESSAGE aquaman xyz java-programming Java is based on C++!
response:
ERROR (Wrong password)

Get messages
GET-MESSAGES mary poppins 0 java-programming
response:
ERROR (User not in room)

Get messages
GET-MESSAGES superman clarkkent 0 c-programming
response:
ERROR (User not in room)

Get messages from 0
GET-MESSAGES mary poppins 10000 c-programming
response:
NO-NEW-MESSAGES

LEAVE-ROOM mary poppins c-programming
response:
OK

Get messages from 2
GET-MESSAGES superman clarkkent 4 java-programming
response:
ERROR (User not in room)

Killing Server
"""
]

if __name__ == '__main__':
    main()
