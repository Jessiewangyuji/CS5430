import sys
from datetime import datetime
TIME_WINDOW = 600
LOGIN_ATTEMPT = 10
LOGIN_ATTEMPT_ALREADY_LOGEDIN = 3

logpath = sys.argv[1]

failure_time = {}
user_attack = []
login = []
now = datetime.now()
curryear = now.year
with open(logpath, "r") as log:
    for line in log:
        if "authentication failure" in line:
            time = line.split(" ")[0:3]
            user = line.split(" ")[-1] #TODO:user + uid?
            user = user.split("=")[-1]
            time = ' '.join(time)
            datetime_obj = datetime.strptime(time, "%b %d %X")
            #assumption: log file is most recent in current year
            datetime_obj = datetime_obj.replace(year = curryear)

            if user in failure_time:
                list = failure_time[user]
                for i in range(0, len(list) - 1):
                    diff = (datetime_obj - list[i]).total_seconds()
                    if diff > TIME_WINDOW: #10-minute time window
                        del list[i]
                    else:
                        break
                list.append(datetime_obj)
                failure_time[user] = list
                if user not in login and len(list) > LOGIN_ATTEMPT:
                    if user not in user_attack:
                        user_attack.append(user)
                if user in login and len(list) > LOGIN_ATTEMPT_ALREADY_LOGEDIN:
                    if user not in user_attack:
                        user_attack.append(user)
            else:
                list = []
                list.append(datetime_obj)
                failure_time[user] = list
        elif "ssh" in line:
            print "ssh"
            #TODO: ssh
        elif "session closed" in line:
            user = line.split(" ")[-1]
            if user in login:
                del login[login.index(user)]
        elif "New session" in line:
            user = line.split(" ")[-1]
            if user not in login:
                login.append(user)


if len(user_attack) == 0:
    print "OK" #if login is successful
else:
    print "Intrusion" #detect intrusion
    print (str(len(user_attack))+' users might be under attack')
#further estimate the number of users whose accounts the attacker attempted to access
