# Program-mode. Must be one of
#   "setup"     - This will install the required libraries onto your device
#   "calibrate" - This will run a calibration session, allowing you to get min/max values for each sensor
#                 defined in the SENSORS-list below. Make sure you have a glass of water readily available.
#   "repl"      - This will only connect to Wi-Fi allowing you to run commands in the REPL on the device
#   "app"       - This will run the app that and reports sensor values at the configured interval

PROGRAM_MODE = "setup"

# Wi-Fi config
WIFI_SSID = "<your ssid>"
WIFI_PASSWORD = "<your wifi password>"
WIFI_COUNTRY = "<your country>"

# Max analog input value. The resolution of the measured values is 16 bits, so the values are between 0 and 65535
MAX_ADC_VALUE = 65535

# Add sensors here, you can have up to three connected to a single Pico W
SENSORS = [
    {
        # Give the sensor a unique id used to identify it
        "id": "monstera",
        # Which GPIO pin the sensor is connected to (note: not physical pin)
        # Should be either 26 (ADC1), 27 (ADC2), or 28 (ADC3)
        # See https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf
        "pin": 26,
        # Replace with max value after calibrating (or leave as-is)
        "max_value": MAX_ADC_VALUE,
        # Replace with min value after calibrating (or leave as-is)
        "min_value": 0,
    },
]

# How long to (deep) sleep between updates (in seconds)
UPDATE_INTERVAL = 60 * 30

SANITY_CONFIG = {
    # Replace "<project id>" with your projectId
    "projectId": "<project id>",
    # Replace "<dataset>" with your dataset
    "dataset": "<dataset>",
    # Create a write-token at https://www.sanity.io/manage/project/<your-projectid>/api
    "token": "<token>",
    # Change this to current date, see https://www.sanity.io/docs/api-versioning for more info
    "version": "2023-03-05",
    "useCdn": False,
}
