import asyncio
import websockets
from ktrade import tunnel



if __name__ == '__main__':
    start_server = websockets.serve(tunnel.accept, "localhost", 8765, 
                                    ping_timeout=5, ping_interval=5, compression=None)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
