from sqlalchemy import MetaData, Table, Column, Integer, Text, DateTime, create_engine
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
lines_count = int(os.getenv('LINES_COUNT'))

metadata = MetaData()
engine = create_engine(db_url)
conn = engine.connect()

records = Table('records', metadata,
                Column('record_id', Integer, primary_key=True),
                Column('record_temperature', Text),
                Column('record_wind_speed', Text),
                Column('record_wind_direction', Text),
                Column('record_pressure', Text),
                Column('record_precipitation', Text),
                Column('record_precipitation_level', Text),
                Column('created_on', DateTime(), default=datetime.now),
                Column('updated_on', DateTime(),
                       default=datetime.now, onupdate=datetime.now)
                )

metadata.create_all(engine)


def hpascal_to_mm(hpressure):
    mm_pressure = hpressure * 0.75
    return mm_pressure


def deg_to_direction(deg):
    match deg:
        case (180):
            return "Ю"
        case (0):
            return "С"
        case (90):
            return "В"
        case (270):
            return "З"
        case deg if 0 < deg < 90:
            return "СВ"
        case deg if 90 < deg < 180:
            return "ЮВ"
        case deg if 180 < deg < 270:
            return "ЮЗ"
        case deg if 270 < deg < 360:
            return "СЗ"
        case _:
            return "Not a point"


def detect_precipitation(rain, showers, snowfall):
    if rain == showers == snowfall == 0:
        return 'No precipitation'
    if rain != 0:
        return 'Rain'
    if showers != 0:
        return 'Showers'
    if snowfall != 0:
        return 'Snowfall'


def write_to_db(data):
    insertion_query = records.insert().values([
        {
            'record_temperature': data['current_temperature_2m'],
            'record_wind_speed': data['current_wind_speed_10m'],
            'record_wind_direction': deg_to_direction(int(data['current_wind_direction_10m'])),
            'record_pressure': str(hpascal_to_mm(int(data['current_surface_pressure']))),
            'record_precipitation': detect_precipitation(data['current_rain'], data['current_showers'], data['current_snowfall']),
            'record_precipitation_level': data['current_precipitation'],
        }
    ])
    conn.execute(insertion_query)
    conn.commit()
