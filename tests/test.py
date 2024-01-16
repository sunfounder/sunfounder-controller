#!/usr/bin/env python3
import asyncio
import websockets
import json
import time
import threading

class SunFounderController():

    def __init__(self):
        self.server_thread = threading.Thread(target=self.work)
        self.server_thread.daemon = True
        self.client_num = 0
        self.client = {}

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
        self.server = await websockets.serve(self.handler, "0.0.0.0", 8765)
        print(f'self.server: {type(self.server)}')
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
                    print("websocket.recv() temp: %s" % tmp)
                except asyncio.TimeoutError as e:
                    pass

                # send
                try:
                    # print(json.dumps(self.send_dict))
                    await websocket.send(f'{time.time()}')
                except Exception as e:
                    print('send Exception: %s'%e)

                await asyncio.sleep(0.01)

            except websockets.exceptions.ConnectionClosed as connection_code:
                # disconneted flag
                print(f'{_client_num}: {connection_code}')
                print(f'client {_client_num, _client_ip} disconneted')
                break

        self.client.pop(str(_client_num))
        self.is_closed = True

if __name__ == "__main__":
    sc = SunFounderController()
    sc.start()
    
    while True:
        key = input()
        if key in 'qQ':
            sc.close()
            break


