import pytest
from ktrade import providerdict
from ktrade.protocol import tunnel_pb2
from ktrade import provider



@pytest.fixture
def cybos_rqrs_provider():
    node = tunnel_pb2.Node()
    node.vendor = 'CYBOS'
    node.role = tunnel_pb2.PROVIDER
    node.channel_type = tunnel_pb2.REQ_RES
    node.service = tunnel_pb2.STOCK
    yield node

    providerdict._clear_provider()


@pytest.fixture
def multiple_cybos_rqrs_provider():
    node = tunnel_pb2.Node()
    node.vendor = 'CYBOS'
    node.role = tunnel_pb2.PROVIDER
    node.channel_type = tunnel_pb2.REQ_RES
    node.service = tunnel_pb2.STOCK

    node2 = tunnel_pb2.Node()
    node2.CopyFrom(node)
    node3 = tunnel_pb2.Node()
    node3.CopyFrom(node)

    yield [node, node2, node3]

    providerdict._clear_provider()



@pytest.mark.asyncio
async def test_none_find_provider():
    cybos_provider = await providerdict.find_provider('CYBOS', tunnel_pb2.REQ_RES, tunnel_pb2.STOCK)
    assert cybos_provider is None


@pytest.mark.asyncio
async def test_add_provider(cybos_rqrs_provider):
    cybos_provider = provider.KrossProvider(1, cybos_rqrs_provider)
    await providerdict.add_provider(cybos_provider)

    found = await providerdict.find_provider('CYBOS', tunnel_pb2.REQ_RES, tunnel_pb2.STOCK)
    assert found == cybos_provider


@pytest.mark.asyncio
async def test_busycheck_provider(cybos_rqrs_provider):
    cybos_provider = provider.KrossProvider(1, cybos_rqrs_provider)
    await providerdict.add_provider(cybos_provider)

    cybos_provider.pending = True
    found = await providerdict.find_provider('CYBOS', tunnel_pb2.REQ_RES, tunnel_pb2.STOCK)
    assert found is None


@pytest.mark.asyncio
async def test_no_vendor_provider(cybos_rqrs_provider):
    cybos_provider = provider.KrossProvider(1, cybos_rqrs_provider)
    await providerdict.add_provider(cybos_provider)
    found = await providerdict.find_provider('KIWOOM', tunnel_pb2.REQ_RES, tunnel_pb2.STOCK)
    assert found  is None


@pytest.mark.asyncio
async def test_multi_rqrs_provider(multiple_cybos_rqrs_provider):
    mproviders = []
    for m in multiple_cybos_rqrs_provider:
        cprovider = provider.KrossProvider(1, m)
        mproviders.append(cprovider)
        await providerdict.add_provider(cprovider)

    for i in range(3):
        found = await providerdict.find_provider('CYBOS', tunnel_pb2.REQ_RES, tunnel_pb2.STOCK)
        assert found == mproviders[i]
