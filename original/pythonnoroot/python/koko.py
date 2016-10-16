from bbio import *
import time

def setup(speed=115200):
  # Start Serial2 at speed baud:
  Serial2.begin(speed)

def nacti(): 
    data = ""
    while Serial2.available(): 
        data += Serial2.read()
    return data

def pokus1(color="10"):
    for i in range(15):
        command = "x"+str(i) + " " + color  
        Serial2.write(command + "\n")
        time.sleep(0.01)

def koko(color="10"):
    for i in range(135):
        while Serial2.available(): 
            Serial2.read() 
        command = "x"+str(i) + " " + color 
        Serial2.write(command + "\n")
        #time.sleep(0.008)
        itime = time.time()
        icommand = ""
        while(icommand.count(command)==0 and time.time() < itime + 0.1): 
            icommand += Serial2.read()
        #print icommand

def pokus(): 
    command = "pokus"
    Serial2.write(command + "\n")
    answer = ""
    while Serial2.available(): 
        answer += Serial2.read()
    return answer

