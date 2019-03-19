import RPi.GPIO as gpio
import time as time
from recorder import Recorder
import ftplib
import os


gpio.setmode(gpio.BCM)
gpio.setup(10, gpio.IN, pull_up_down=gpio.PUD_UP)

def sendChat():
    filename ="chat.wav"
    ftp= ftplib.FTP('----HOST----')
    ftp.login("----USERNAME----","----PASSWORD----")
    ftp.cwd('PATH')
    myfile = open('/home/pi/Desktop/nonblocking.wav','rb')
    ftp.storbinary('STOR '+filename, myfile)
    print('sent chat')

def downloadChat():
    global status
    ftp= ftplib.FTP('HOST')
    ftp.login("----USERNAME----","----PASSWORD----")
    ftp.cwd('----PATH----')
    filename ="chat.wav"
 
    # download the file
    
    try:
        ftp.size("chat.wav")
        status=True
    except ftplib.all_errors:
        print("no unread chat")
        status=False
        
    if status:
        local_filename = os.path.join(r"/home/pi/Desktop", filename)
        lf = open(local_filename, "wb")
        ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
        lf.close()
        print("downloaded done")
        os.system('aplay /home/pi/Desktop/chat.wav')
        ftp.delete("chat.wav")
        print("deleted chat")
        
def my_callback(channel):  
    if gpio.input(10):     # if port 10 == 1
        global recfile
        print("Rising edge detected on 10")
        gpio.remove_event_detect(10)
        recfile.stop_recording()
        gpio.add_event_detect(10, gpio.BOTH, callback=my_callback, bouncetime=10)
        sendChat()
        #recfile.close()
        
        
    else:                  # if port 10 != 1
        global recfile
        print("Falling edge detected on 10")
        gpio.remove_event_detect(10)
        rec = Recorder(channels=2)
        recfile = rec.open('nonblocking.wav', 'wb')
        recfile.start_recording()
        gpio.add_event_detect(10, gpio.BOTH, callback=my_callback, bouncetime=10)



gpio.add_event_detect(10, gpio.BOTH, callback=my_callback, bouncetime=10)


while True:
    time.sleep(2)
    downloadChat()
    if(gpio.input(10) == False):
       print("Button Pressed")
       
    else:
       print("listening")
      

try:
    print(gpio.input(10))

except KeyboardInterrupt:
    gpio.cleanup()
gpio.cleanup()