import time
from machine import Pin, ADC
from config import SENSORS, MAX_ADC_VALUE

SAMPLES = 20


def run(pin=None):
    results = {}

    for i, sensor in enumerate(
        [sensor for sensor in SENSORS if not pin or pin is sensor["pin"]]
    ):
        min = MAX_ADC_VALUE
        max = 0
        for n in range(SAMPLES):
            current = ADC(Pin(sensor["pin"], mode=Pin.IN)).read_u16()
            if current < min:
                min = current
            if current > max:
                max = current
            print(
                f"[calibrating {i + 1} of {len(SENSORS)}] {sensor['id']}: current: {current}, min: {min}, max: {max} ({SAMPLES - n} samples left)"
            )
            time.sleep(1)

        results[sensor["id"]] = {"pin": sensor["pin"], "min": min, "max": max}

    print("Done")

    for sensor_id in results:
        print(
            f"{sensor_id} (pin: {results[sensor_id]['pin']}): min: {results[sensor_id]['min']}, max: {results[sensor_id]['max']}"
        )
