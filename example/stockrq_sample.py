import asyncio
from datetime import datetime
from ktrade import service
from ktrade.protocol import tunnel_pb2
from ktrade.protocol import stock_pb2
from google.protobuf.timestamp_pb2 import Timestamp


def do_response(data, **kwargs):
    print('get request')
    query = stock_pb2.StockQuery()
    try:
        query.ParseFromString(data)
        query_type = query.WhichOneof('query')
        if query_type == 'day_query':
            pass
    except:
        print('Cannot parse')


async def main():
    stock_service = await service.stock_provider_service("CYBOS", tunnel_pb2.REQ_RES, callback=do_response)

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
