import sys
from datetime import datetime
from sets import Set
TIME_WINDOW = 600
SSH_TIME_WINDOW = 60 * 120
SSH_NUM_IP = 1
LOGIN_ATTEMPT = 10
LOGIN_ATTEMPT_ALREADY_LOGEDIN = 3
SUDO_ATTEMPT = 5

logpath = sys.argv[1]
failure_time = {}
user_attack = []
ssh_user_attack = {}
login = []
ssh_ip_access_time = {}
ssh_ip_access_user = {}
now = datetime.now()
curryear = now.year
with open(logpath, "r") as log:
    for line in log:
        now = datetime.now()
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
                i = 0
                while i < len(list):
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
        elif "sshd" in line:
            time = line.split(" ")[0:3]
            time = ' '.join(time)
            datetime_obj = datetime.strptime(time, "%b %d %X")
            datetime_obj = datetime_obj.replace(year = curryear)
            if "maximum authentication attempts exceeded" in line:
                line_split = line.split(" ")
                ip = line_split[line_split.index("port") - 1]
                username = line_split[line_split.index("from") - 1]
                if ip in ssh_user_attack:
                    ssh_user_attack[ip].add(username)
                else:
                    userset = set([username])
                    ssh_user_attack[ip] = userset
            elif "port" in line and "password" in line:
                line_split = line.split(" ")
                ip = line_split[line_split.index("port") - 1]
                username = line_split[line_split.index("from") - 1]
                if ip in ssh_ip_access_time:
                    timelist = ssh_ip_access_time[ip]
                    userlist = ssh_ip_access_user[ip]
                    i = 0
                    while i < len(timelist):
                        if (datetime_obj - timelist[i]).total_seconds > SSH_TIME_WINDOW:
                            del timelist[i]
                            del userlist[i]
                        else:
                            break
                else:
                    timelist = []
                    userlist = []
                timelist.append(datetime_obj)
                userlist.append(username)
                if len(set(userlist)) > SSH_NUM_IP:
                    ssh_user_attack[ip] = set(userlist)
                ssh_ip_access_time[ip] = timelist
                ssh_ip_access_user[ip] = userlist
        elif "sudo" in line:
            if "incorrect password attempts" in line:
                line_split = line.split(" ")
                num_incorrect = int(line_split[line_split.index("incorrect") - 1])
                if num_incorrect > SUDO_ATTEMPT:
                    user_index = line_split.index("sudo:") + 1
                    while user_index < len(line_split):
                        if line_split[user_index] == "":
                            user_index += 1
                        else:
                            break
                    user_attack.append(line_split[user_index])
        elif "session closed" in line and "sshd" not in line:
            user = line.split(" ")[-1]
            if user in login:
                del login[login.index(user)]
        elif "session closed" in line and "sshd" in line:
            line_split = line.split(" ")
            user = line_split[line_split.index("user") + 1]
            if user in login:
                del login[login.index(user)]
        elif "New session" in line:
            user = line.split(" ")[-1]
            if user not in login:
                login.append(user)
        elif "session opened" in line:
            line_split = line.split(" ")
            user = line_split[line_split.index("user") + 1]
            login.append(user)

###syslog format!!!
if len(user_attack) == 0 and len(ssh_user_attack) == 0:
    print "OK" #if login is successful
else:
    print "Intrusion" #detect intrusion
    user_attacked_set = set()
    for i in ssh_user_attack:
        user_attacked_set = user_attacked_set|ssh_user_attack[i]
    for i in user_attack:
        user_attacked_set.add(i)
    print (str(len(user_attacked_set))+' users might be under attack')
#further estimate the number of users whose accounts the attacker attempted to access
