import os
import time

import ubinascii
import urequests
from machine import Pin, ADC, unique_id, deepsleep
from usanity import mutate_request
from usanity.mutations import (
    create_if_not_exists,
    patch,
    patch_set,
    set_if_missing,
    unset,
    insert,
)

from config import (
    SANITY_CONFIG,
    SENSORS,
    WIFI_COUNTRY,
    WIFI_PASSWORD,
    WIFI_SSID,
    UPDATE_INTERVAL,
)
from get_vsys import get_vsys
from json_datetime import json_datetime
from wifi import connect_blink

# Device info
[sysname, nodename, release, version, machine] = os.uname()

# Get the device id
device_id = ubinascii.hexlify(unique_id()).decode("utf-8")

print(f"device id is {device_id}")


def is_battery(vsys):
    return vsys < 3.5


def get_battery_sensor_mutations(power, current_time):
    (year, month, day, hour, minute, second, wd, yd) = current_time
    timestamp = json_datetime(year, month, day, hour, minute, second)

    sensor_uuid = f"sensor-{device_id}-battery"

    device_name = f"{sysname} {nodename} {release} {version} {machine}"

    return [
        create_if_not_exists({"_id": sensor_uuid, "_type": "sensor"}),
        patch(sensor_uuid, patch_set("type", "battery")),
        patch(sensor_uuid, patch_set("name", device_name)),
        patch(
            sensor_uuid,
            patch_set("latest", {"timestamp": timestamp, "value": power / 3}),
        ),
        patch(sensor_uuid, set_if_missing("measurements", [])),
        patch(sensor_uuid, unset(f'measurements[_key=="{timestamp}"]')),
        patch(
            sensor_uuid,
            insert(
                "measurements",
                "before",
                0,
                [{"_key": timestamp, "value": power, "timestamp": timestamp}],
            ),
        ),
        # cap measurements at 200 entries
        patch(sensor_uuid, unset("measurements[200:]")),
    ]


def normalize_moisture_value(value: int, min: int, max: int):
    return (value - min) / (max - min)


def get_sensor_mutations(measurement):
    (year, month, day, hour, minute, second, wd, yd) = measurement["time"]
    timestamp = json_datetime(year, month, day, hour, minute, second)

    sensor_uuid = f"sensor-{device_id}-{measurement['sensor_id']}"

    return [
        create_if_not_exists({"_id": sensor_uuid, "_type": "sensor"}),
        patch(sensor_uuid, patch_set("type", "moisture")),
        patch(sensor_uuid, patch_set("name", measurement["sensor_id"])),
        patch(
            sensor_uuid,
            patch_set(
                "latest", {"timestamp": timestamp, "value": measurement["value"]}
            ),
        ),
        patch(sensor_uuid, set_if_missing("measurements", [])),
        patch(sensor_uuid, unset(f'measurements[_key=="{timestamp}"]')),
        patch(
            sensor_uuid,
            insert(
                "measurements",
                "before",
                0,
                [
                    {
                        "_key": timestamp,
                        "value": measurement["value"],
                        "timestamp": timestamp,
                    }
                ],
            ),
        ),
        # cap measurements at 200 entries
        patch(sensor_uuid, unset("measurements[200:]")),
    ]


def submit_mutations(mutations: list):
    (url, headers, body) = mutate_request(
        project_id=SANITY_CONFIG["projectId"],
        dataset=SANITY_CONFIG["dataset"],
        api_version=SANITY_CONFIG["version"],
        token=SANITY_CONFIG["token"],
        mutations=mutations,
    )

    try:
        res = urequests.post(url, json=body, headers=headers)

        print(f"Successfully posted sensor values {res.text}")
        res.close()
    except Exception as e:
        print(f"Could not post status: {e}")


def read_measurements(sensors: list, current_time):
    return [
        {
            "sensor_id": sensor["id"],
            "value": normalize_moisture_value(
                ADC(Pin(sensor["pin"], mode=Pin.IN)).read_u16(),
                min=sensor["min_value"],
                max=sensor["max_value"],
            ),
            "time": current_time,
        }
        for sensor in sensors
    ]


def flatten(xxs: list):
    return [x for xs in xxs for x in xs]


while True:
    vsys = get_vsys()

    onboard_led = Pin("LED", Pin.OUT)
    connect_blink(onboard_led, WIFI_SSID, WIFI_PASSWORD, WIFI_COUNTRY)

    current_time = time.localtime()

    measurements = read_measurements(SENSORS, current_time)
    sensor_mutations = flatten(
        [get_sensor_mutations(measurement) for measurement in measurements]
    )
    battery_status_mutations = (
        get_battery_sensor_mutations(vsys, current_time) if is_battery(vsys) else []
    )

    submit_mutations(sensor_mutations + battery_status_mutations)

    # Needed before deepsleep to avoid crash
    time.sleep(1)

    if is_battery(vsys):
        # deepsleep if battery powered
        print(f"Deep sleep for {UPDATE_INTERVAL} seconds")
        deepsleep(UPDATE_INTERVAL * 1000)
    else:
        # likely USB powered, sleep normally
        print(f"Sleep for {UPDATE_INTERVAL} seconds")
        time.sleep_ms(UPDATE_INTERVAL * 1000)
    print(f"Wake up!")
