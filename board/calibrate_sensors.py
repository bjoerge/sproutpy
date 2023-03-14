import time
from machine import Pin, ADC
import config

SAMPLES = 20


def run(pin=None):
    sensors_with_pins = [
        {
            "id": sensor["id"],
            "pin": sensor["pin"],
            "adc": ADC(Pin(sensor["pin"], mode=Pin.IN)),
        }
        for sensor in config.SENSORS
        if not pin or pin is sensor["pin"]
    ]

    results = {}

    for i, sensor in enumerate(sensors_with_pins):
        min = config.MAX_ADC_VALUE
        max = 0
        for n in range(SAMPLES):
            current = ADC(Pin(16, mode=Pin.IN)).read_u16()
            if current < min:
                min = current
            if current > max:
                max = current
            print(
                f"[calibrating {i + 1} of {len(sensors_with_pins)}] {sensor['id']}: current: {current}, min: {min}, max: {max} ({SAMPLES - n} samples left)"
            )
            time.sleep(1)

        results[sensor["id"]] = {"pin": sensor["pin"], "min": min, "max": max}

    print("Done")

    for sensor_id in results:
        print(
            f"{sensor_id} (pin: {results[sensor_id]['pin']}): min: {results[sensor_id]['min']}, max: {results[sensor_id]['max']}"
        )
