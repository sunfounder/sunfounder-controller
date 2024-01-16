import asyncio
import websockets
import json
import time
import threading

class SunFounderController():
    PORT = 8765

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
    

    def __init__(self, port=PORT):
        self.port = port
        self.server_thread = threading.Thread(target=self.work)
        self.server_thread.daemon = True
        self.client_num = 0
        self.client = {}
        self.is_received = False

    def start(self):
        self.work_flag = True
        self.server_thread.start()

    def close(self):
        self.server.close()
        self.work_flag = False
        # print('close done1')
        # print( self.server_thread.is_alive())
        # self.server_thread.join()
        while len(self.client):
            time.sleep(0.01)
        print('close done')

    def work(self):
        asyncio.run(self.main())

    async def main(self):
        self.server = await websockets.serve(self.handler, "0.0.0.0", self.port)
        print(f'websocket server start at port {self.port}')
        async with self.server:
            await asyncio.Future() # run forever
        print('server closed')

    async def handler(self, websocket):
        _client_num = self.client_num
        _client_ip = websocket.remote_address[0]
        self.client_num  += 1
        self.client[str(_client_num)] = _client_ip
        print(f'client {_client_num, _client_ip} conneted')
        # print(websocket.remote_address)

        while self.work_flag:
            try:
                # recv
                try:
                    tmp = await asyncio.wait_for(websocket.recv(), timeout=0.001)
                    # print("websocket.recv() temp: %s" % tmp)
                except asyncio.TimeoutError as e:
                    # print('asyncio.TimeoutError : %s'%e)
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
                    self.is_received = False
                    print("JSONDecodeError")
                except Exception as e:
                    pass

                await asyncio.sleep(0.01)

            except websockets.exceptions.ConnectionClosed as connection_code:
                # disconneted flag
                print(f'{_client_num}: {connection_code}')
                print(f'client {_client_num, _client_ip} disconneted')
                break

        self.client.pop(str(_client_num))
        self.is_closed = True

    def data_processing(self):
        if self.recv_dict['Heart'] == 'ping':
            self.send_dict['Heart'] = 'pong'

    def start_work(self):
        print('Start!')
        self.loop.run_forever()


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


if __name__ == "__main__":
    sc = SunFounderController()
    sc.start()
    
    try:
        while True:
            if sc.is_received is True:
                # get
                print(sc.recv_dict)
                # set       
                sc.send_dict = 'ok'

            time.sleep(0.1)
    finally:
        sc.close()


