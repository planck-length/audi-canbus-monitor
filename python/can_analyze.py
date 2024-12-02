from pathlib import Path
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from configparser import ConfigParser
from cantools import database

import sys

if len(sys.argv) > 1:
    SOCKET = sys.argv[1]
else:
    SOCKET = "vcan0"

home = Path(__file__).parent

db = database.load_file(home / "vw_mqb_2010.dbc")

influx_db_config = home.parent / "influxdb2/influx-configs"

config = ConfigParser()
config.read(influx_db_config)

token = config["default"]["token"].strip('"')

org = config["default"]["org"].strip('"')
url = "http://localhost:8086"
bucket = "can_monitoring"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)
from datetime import datetime

import can

while True:
    with can.interface.Bus(SOCKET, interface="socketcan") as can_bus:
        message = can_bus.recv()
        timestamp = datetime.fromtimestamp(message.timestamp)
        # breakpoint()
        dict_structure = {
            "measurement": "can_messages",
            "tags": {"arbitration_id": message.arbitration_id},
            "fields": {"data": message.data.hex()},
            # "time": timestamp
        }
        point = Point.from_dict(dict_structure)

        write_api.write(bucket=bucket, org=org, record=point)

        try:
            decoded_message = db.decode_message(message.arbitration_id, message.data)
            dict_structure = {
                "measurement": message.arbitration_id,
                "fields": dict(decoded_message.items()),
                # "time":  timestamp
            }
            # breakpoint()
            point = Point.from_dict(dict_structure)
            write_api.write(bucket=bucket, org=org, record=point)
        except KeyError:
            pass
            # print("Message not found in database")
        except database.errors.DecodeError as err:
            print(f"Decode error: {err}")

        except ValueError as err:
            print(f"Value error: {err}")
