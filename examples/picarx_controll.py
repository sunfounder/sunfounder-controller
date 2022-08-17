from picarx import Picarx
from robot_hat import utils, Music
from vilib import Vilib
import os
from time import sleep

utils.reset_mcu()
sleep(0.5)

# get IP address
def getIP():
    wlan0 = os.popen("ifconfig wlan0 |awk '/inet/'|awk 'NR==1 {print $2}'").readline().strip('\n')
    eth0 = os.popen("ifconfig eth0 |awk '/inet/'|awk 'NR==1 {print $2}'").readline().strip('\n')

    if wlan0 == '':
        wlan0 = None
    if eth0 == '':
        eth0 = None

    return wlan0,eth0

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

music = Music()

def horn(): 
    status, result = utils.run_command('sudo killall pulseaudio')
    music.sound_effect_threading('./sounds/car-double-horn.wav')
    

def main():

    speed = 50

    sc = SunFounderController()
    sc.set_name('Picarx-001')
    sc.set_type('Picarx')
    sc.start()

    px = Picarx()
  

    wlan0,eth0 = getIP()
    if wlan0 != None:
        ip = wlan0
    else:
        ip = eth0
    print('ip : %s'%ip)

    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=False, web=True)
         
    while True:

        sleep(0.2)

        # send data 
        sc.set('video','http://'+ip+':9000/mjpg')
        sc.set("A", speed)
        sc.set("E", speed)

        grayscale_data = px.get_grayscale_data()
        # print(px.get_grayscale_data())
        sc.set("D", [ grayscale_data[2], grayscale_data[1], grayscale_data[0]] )
        
        distance = px.get_distance()
        sc.set("L", [0,distance])
        sc.set("M", distance)


        # print(sc.send_dict)
        
        # get data   
        # recv = sc.getall()
        # print(recv)     

        if sc.get('J') == True:
            horn()

        Joystick_K_Val = sc.get('K')
        if Joystick_K_Val != None:
            dir_angle = map(Joystick_K_Val[0], -100, 100, -45, 45)
            speed = Joystick_K_Val[1]
            px.set_dir_servo_angle(dir_angle)
            if speed > 0:
                px.forward(speed)
            elif speed < 0:
                speed = -speed
                px.backward(speed)
            else:
                px.stop()

            
        if sc.get('N') == True:
            Vilib.color_detect("red")
        else:
            Vilib.color_detect_switch(False)

        if sc.get('O') == True:
            Vilib.human_detect_switch(True)  
        else:
            Vilib.human_detect_switch(False)  

        if sc.get('P') == True:
            Vilib.object_detect_switch(True) 
        else:
            Vilib.object_detect_switch(False)

        
        Joystick_Q_Val = sc.get('Q')
        if Joystick_Q_Val != None:
            # pan = map(Joystick_Q_Val[0], -100, 100, -90, 90)
            # tilt = map(Joystick_Q_Val[1], -100, 100, -35, 75)
            pan = min(90,max(-90,Joystick_Q_Val[0]))
            tilt = min(75, max(-35, Joystick_Q_Val[1]))
            px.set_camera_servo1_angle(tilt)
            px.set_camera_servo2_angle(pan)


def servos_test():
    px = Picarx()
    px.set_camera_servo1_angle(0)
    px.set_camera_servo2_angle(0)
    sleep(0.5)

    while True:
        for angle in range(0,75):
            px.set_camera_servo1_angle(angle)
            sleep(0.01)
        for angle in range(75,-35,-1):
            px.set_camera_servo1_angle(angle)
            sleep(0.01)        
        for angle in range(-35,0):
            px.set_camera_servo1_angle(angle)
            sleep(0.01)

        # px.set_camera_servo1_angle(75)
        # px.set_camera_servo2_angle(0)



if __name__ == "__main__":
    main()
    # servos_test()
    # while True:
    #     horn()
    #     sleep(1)  


