from sunfounder_controller import SunFounderController
from picrawler import Picrawler
from robot_hat import Ultrasonic
from time import sleep
import json

def main():
    sc = SunFounderController()
    sc.start()
    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]) 


    while True:

        # send data 
        for value in range(0, 100, 10):         
            sc.set("A_region", value)

            # get data          
            k_val = sc.get('K_region')
            print("k_val:",k_val)

            # control
            if k_val == 'forward':
                crawler.do_action('forward',2,90)  
        
            if k_val == 'backward':
                crawler.do_action('backward',2,90) 

            if k_val == 'left':
                crawler.do_action('turn left',2,90) 

            if k_val == 'right':
                crawler.do_action('turn right',2,90)   
            
            sleep(1)

 
if __name__ == "__main__":
    main()