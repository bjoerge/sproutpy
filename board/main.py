from config import PROGRAM_MODE

# Uncomment one of the below to run in different modes
if PROGRAM_MODE == "setup":
    from setup import run

    run()
elif PROGRAM_MODE == "app":
    import app

elif PROGRAM_MODE == "calibrate":
    from calibrate_sensors import run

    run()
elif PROGRAM_MODE == "repl":
    from config import WIFI_SSID, WIFI_PASSWORD, WIFI_COUNTRY
    import wifi

    wifi.connect(ssid=WIFI_SSID, password=WIFI_PASSWORD, country=WIFI_COUNTRY)
