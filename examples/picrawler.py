from sunfounder_controller import SunFounderController
from picrawler import Picrawler
from robot_hat import Pin, Ultrasonic, utils
from vilib import Vilib
import os
from time import sleep

utils.reset_mcu()
sleep(0.5)

# IP address
def getIP():
    wlan0 = os.popen("ifconfig wlan0 |awk '/inet/'|awk 'NR==1 {print $2}'").readline().strip('\n')
    eth0 = os.popen("ifconfig eth0 |awk '/inet/'|awk 'NR==1 {print $2}'").readline().strip('\n')

    if wlan0 == '':
        wlan0 = None
    if eth0 == '':
        eth0 = None

    return wlan0,eth0

def main():
    sc = SunFounderController()
    sc.set_name('picrawler-002')
    sc.set_type('Picrawler')
    sc.start()
    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]) 
    sonar = Ultrasonic(Pin("D2") ,Pin("D3"))

    wlan0,eth0 = getIP()
    if wlan0 != None:
        ip = wlan0
    else:
        ip = eth0
    print('ip : %s'%ip)

    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display()
         
    while True:
        print(sc.send_dict)
        # send data 
        distance = sonar.read()
        sc.set("D",[0,distance])
        sc.set('video','http://'+ip+':9000/mjpg')

        # get data   
        recv = sc.getall()
        print(recv)     

        k_val = sc.get('K')
        if k_val != None:
            print("k_val:",k_val)

        A_val = sc.get('A')
        if A_val != None:
            print("Ak_val:",A_val)

        # control
        if k_val == 'forward':
            crawler.do_action('forward',2,A_val)     
        if k_val == 'backward':
            crawler.do_action('backward',2,A_val) 
        if k_val == 'left':
            crawler.do_action('turn left',2,A_val) 
        if k_val == 'right':
            crawler.do_action('turn right',2,A_val)         
        sleep(1)

 
if __name__ == "__main__":
    main()