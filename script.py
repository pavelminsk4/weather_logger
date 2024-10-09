from database import write_to_db
from dotenv import load_dotenv
from export_to_xlsx import exp_to_xlsx
from weather import fetch_weather
import aioconsole
import asyncio
import os

load_dotenv()
upd_time = int(os.getenv('UPDATE_TIME_SEC'))


async def export():
    while True:
        inp = await aioconsole.ainput('Enter "export" to create Excel document - ')
        if inp == 'export':
            exp_to_xlsx()
        else:
            print('Enter correct command!')


async def fetch():
    while True:
        data = fetch_weather()
        write_to_db(data)
        await asyncio.sleep(upd_time)


async def logger():
    task1 = asyncio.create_task(export())
    task2 = asyncio.create_task(fetch())

    await task1
    await task2


asyncio.run(logger())
