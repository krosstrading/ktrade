import asyncio
from datetime import datetime
from ktrade import service
from ktrade.protocol import tunnel_pb2
from ktrade.protocol import stock_pb2
from google.protobuf.timestamp_pb2 import Timestamp


async def subscribe_data_arrived(data, **kwargs):
    pass

async def main():
    stock_service = await service.stock_service("CYBOS", tunnel_pb2.REQ_RES)
    stock_subscribe_service = await service.stock_service("CYBOS",
                                    tunnel_pb2.PUBLISH_SUBSCRIBE,
                                    callback=subscribe_data_arrived)
    
    query = stock_pb2.StockQuery()
    query.day_query.code = 'A005930'
    query.day_query.from_datetime.FromDatetime(datetime(2021, 3, 9))
    query.day_query.until_datetime.FromDatetime(datetime(2021, 3, 9))

    print('send day query')
    result = await stock_service.get_day_data(query)
    print('result', result)
    await stock_subscribe_service.subscribe_stock('A005930')


asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
