import asyncio
import websockets
import json
import time
import os
import threading

class SunFounderController():

    
    recv_flag = False

    send_dict = {
        'Name': '',
        'Type': 'PICO-4WD Car',
        'Check': 'SunFounder Controller',
        }

    recv_dict = {
        'A_region': None,
        'B_region': None,
        'C_region': None,
        'D_region': None,
        'E_region': None,
        'F_region': None,
        'G_region': None,
        'H_region': None,
        'I_region': None,
        'J_region': None,
        'K_region': None,
        'L_region': None,
        'M_region': None,
        'N_region': None,
        'O_region': None,
        'P_region': None,
        'Q_region': None,
    }
    

    def __init__(self):
        start_server = websockets.serve(self.main, "0.0.0.0", 8765)
        tasks = asyncio.wait([start_server])
        self.tasks = asyncio.ensure_future(tasks)
        self.loop = asyncio.get_event_loop()
        self.thread = threading.Thread(target=self.start_work, name="Websocket_thread")

    async def main(self, websocket, path):
        while 1:
            await websocket.send(json.dumps(self.send_dict))
            tmp = await websocket.recv()
            # print("websocket.recv() temp: %s" % tmp)
            try:
                tmp = json.loads(tmp)
                if isinstance(tmp, dict):
                    self.recv_dict = tmp
                    self.recv_flag = True
                else:
                    print("JSONDecodeError")
            except json.decoder.JSONDecodeError:
                print("JSONDecodeError")
            await asyncio.sleep(0.01)

    def start_work(self):
        print('Start!')
        self.loop.run_forever()
    

    def start(self):
        self.thread.start()

    def get(self,key='A_region', default=None):
        # if not isinstance(self.recv_dict, dict):
        #     raise ValueError("recv_dict type error. type '%s', value: '%s'" % (type(self.recv_dict), self.recv_dict))
        return self.recv_dict.get(key, default)

    def set(self,key='A_region', value=None):
        self.send_dict[key] = value




if __name__ == "__main__":
    sc = SunFounderController()
    sc.start()
    
    while True:
        if sc.recv_flag is True:
            # get
            print(sc.get('K_region'))
            # set
            for value in range(0, 100, 10):         
                sc.set("A_region", value)
        time.sleep(2)


