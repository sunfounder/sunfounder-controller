from sunfounder_controller import SunFounderController
from vilib import Vilib
import os
from time import sleep

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

    wlan0,eth0 = getIP()
    if wlan0 != None:
        ip = wlan0
    else:
        ip = eth0

    Vilib.camera_start(inverted_flag=True)
    Vilib.display()
    sc.set('video','http://'+ip+':9000/mjpg')



    print(sc.send_dict)

    while True:

        sc.set('video','http://'+ip+':9000/mjpg')

        # get data 
        for key in sc.send_dict.keys():
            value = sc.get(key)
            # print('%s : %s'%(key,value))

        sleep(0.1)
        
if __name__ == "__main__":
    main()