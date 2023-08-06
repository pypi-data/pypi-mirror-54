# -*- coding:utf-8 -*-
'''
Provides connection to ATAG One Thermostat REST API

#__version__ = '0.1.5'
__all__ = ["pyatag"]

from pytag.gateway import AtagDataStore
'''
import asyncio
from contextlib import suppress
from .helpers import insert_in_db
# import pprint


async def test(loop=None):
    """Test connection with imported TESTDATA dict"""
    from pyatag.gateway import AtagDataStore
    import aiohttp
    from .input import TESTDATA, SQLSERVER
    # pretty = pprint.PrettyPrinter(indent=2)
    async with aiohttp.ClientSession() as session:
        atag = AtagDataStore(host=TESTDATA["_host"],
                             port=TESTDATA["_port"],
                             # mail=None, # test with mail == None
                             mail=TESTDATA["_mail"],
                             interface=None,  # TESTDATA["_interface"],
                             session=session)
        print("Starting loop")
        while True:
            await atag.async_update()
            print('Updated now: {}'.format(atag.sensordata['date_time']))
            # assert atag.paired
            await insert_in_db(atag.sensordata, SQLSERVER, LOOP)
            print("sleeping 3s")
            await asyncio.sleep(3)


async def main(loop=None):
    """Start infinite polling loop"""
    task = asyncio.Task(test(loop=LOOP))
    await asyncio.sleep(300)
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task

try:
    LOOP = asyncio.new_event_loop()
    asyncio.set_event_loop(LOOP)
    LOOP.run_until_complete(main(loop=LOOP))
finally:
    LOOP.run_until_complete(LOOP.shutdown_asyncgens())
    LOOP.close()
