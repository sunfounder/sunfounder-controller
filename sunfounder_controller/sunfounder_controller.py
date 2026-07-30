import asyncio
import websockets
import json
import time
import threading
import os

# Debug logging controlled by env var SF_CONTROLLER_DEBUG=1
_DEBUG = os.environ.get('SF_CONTROLLER_DEBUG', '0') == '1'

def _debug(msg):
    """Print debug message with timestamp if debug mode is on."""
    if _DEBUG:
        print(f'[SF_CONTROLLER_DEBUG] {time.strftime("%H:%M:%S")} {msg}')


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
        _debug(f'client {_client_num, _client_ip} connected, total clients: {self.client_num}')
        _debug(f'websocket headers: {dict(websocket.request_headers)}')

        msg_count = 0
        while self.work_flag:
            try:
                # recv
                tmp = None
                recv_bytes = 0
                try:
                    tmp = await asyncio.wait_for(websocket.recv(), timeout=0.001)
                    recv_bytes = len(tmp.encode('utf-8')) if isinstance(tmp, str) else len(tmp)
                    _debug(f'[RECV] client={_client_num} bytes={recv_bytes} raw={repr(tmp)[:500]}')
                except asyncio.TimeoutError:
                    pass
                except Exception as e:
                    _debug(f'[RECV ERROR] client={_client_num} exception={type(e).__name__}: {e}')
                    raise

                # send
                send_payload = json.dumps(self.send_dict)
                send_bytes = len(send_payload.encode('utf-8'))
                try:
                    await websocket.send(send_payload)
                    if msg_count == 0 or _DEBUG:
                        _debug(f'[SEND] client={_client_num} bytes={send_bytes} payload={repr(send_payload)[:200]}')
                except Exception as e:
                    _debug(f'[SEND ERROR] client={_client_num} exception={type(e).__name__}: {e}')
                    print('send Exception: %s'%e)

                # parse recv data
                if tmp is not None:
                    try:
                        tmp = json.loads(tmp)
                        if isinstance(tmp, dict):
                            self.recv_dict = tmp
                            self.is_received = True
                            self.data_processing()
                            _debug(f'[PARSED] client={_client_num} keys={list(tmp.keys())} heart={tmp.get("Heart","N/A")}')
                        else:
                            _debug(f'[PARSE ERROR] client={_client_num} not a dict: {type(tmp).__name__}')
                            print("JSONDecodeError")
                    except json.decoder.JSONDecodeError:
                        self.is_received = False
                        _debug(f'[PARSE ERROR] client={_client_num} JSONDecodeError')
                        print("JSONDecodeError")
                    except Exception as e:
                        _debug(f'[PARSE ERROR] client={_client_num} {type(e).__name__}: {e}')

                msg_count += 1
                await asyncio.sleep(0.01)

            except websockets.exceptions.ConnectionClosed as connection_code:
                # disconneted flag
                _debug(f'[CLOSE] client={_client_num} code={connection_code} total_msgs={msg_count}')
                print(f'{_client_num}: {connection_code}')
                print(f'client {_client_num, _client_ip} disconneted')
                break
            except Exception as e:
                _debug(f'[HANDLER ERROR] client={_client_num} {type(e).__name__}: {e}')
                raise

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


