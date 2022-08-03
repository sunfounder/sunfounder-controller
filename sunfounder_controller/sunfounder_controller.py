import asyncio
import websockets
import json
import time
import os
import threading

class SunFounderController():

    send_dict = {
        'Name': '',
        'Type': None,
        'Check': 'SunFounder Controller',
        }

    recv_dict = {
        'A': None,
        'B': None,
        'C': None,
        'D': None,
        'E': None,
        'F': None,
        'G': None,
        'H': None,
        'I': None,
        'J': None,
        'K': None,
        'L': None,
        'M': None,
        'N': None,
        'O': None,
        'P': None,
        'Q': None,
        'Heart':None
    }
    

    def __init__(self):
        start_server = websockets.serve(self.main, "0.0.0.0", 8765)
        tasks = asyncio.wait([start_server])
        self.tasks = asyncio.ensure_future(tasks)
        self.loop = asyncio.get_event_loop()
        self.thread = threading.Thread(target=self.start_work, name="Websocket_thread")
        self.is_received = False
        self.started = False
        
    async def main(self, websocket, path):
        print('client conneted')
        while self.started:
            try:
                # recv
                try:
                    tmp = await asyncio.wait_for(websocket.recv(), timeout=0.001)
                    # print("websocket.recv() temp: %s" % tmp)
                except asyncio.TimeoutError as e:
                    # log('asyncio.TimeoutError : %s'%e)
                    pass

                # send
                try:
                    # print(json.dumps(self.send_dict))
                    await websocket.send(json.dumps(self.send_dict))
                except Exception as e:
                    print('send Exception: %s'%e)

                # 
                try:
                    tmp = json.loads(tmp)
                    if isinstance(tmp, dict):
                        self.recv_dict = tmp
                        self.is_received = True
                        self.data_processing()
                    else:
                        print("JSONDecodeError")
                except json.decoder.JSONDecodeError:
                    print("JSONDecodeError")
                except Exception as e:
                    pass

                await asyncio.sleep(0.01)

            except websockets.exceptions.ConnectionClosed as connection_code:
                # disconneted flag
                print(connection_code)
                print('client disconneted')
                break
        print("Websocket main Closed")

    def data_processing(self):
        if self.recv_dict['Heart'] == 'ping':    
            self.send_dict['Heart'] = 'pong'

    def start_work(self):
        print('Start!')
        self.loop.run_forever()
    

    def start(self):
        self.started = True
        self.thread.start()

    def get(self,key='A', default=None):
        # if not isinstance(self.recv_dict, dict):
        #     raise ValueError("recv_dict type error. type '%s', value: '%s'" % (type(self.recv_dict), self.recv_dict))
        return self.recv_dict.get(key, default)

    def getall(self):
        return self.recv_dict
        
    def set(self,key='A_region', value=None):
        self.send_dict[key] = value

    def set_name(self,name:str=None):
        self.send_dict['Name'] = name

    def set_type(self,type:str=None):
        self.send_dict['Type'] = type

    def close(self):
        self.started = False
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.call_soon_threadsafe(self.loop.close)

if __name__ == "__main__":
    sc = SunFounderController()
    sc.start()
    
    while True:
        if sc.is_received is True:
            # get
            print(sc.recv_dict)
            # set       
            sc.send_dict = 'ok'

        time.sleep(0.1)


