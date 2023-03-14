def run():
    print("Setting up…")
    from wifi import connect_blink

    from machine import Pin

    from config import (
        WIFI_COUNTRY,
        WIFI_PASSWORD,
        WIFI_SSID,
    )

    onboard_led = Pin("LED", Pin.OUT)
    connect_blink(onboard_led, WIFI_SSID, WIFI_PASSWORD, WIFI_COUNTRY)

    import mip

    mip.install("datetime")
    mip.install("github:bjoerge/usanity", version="v0.2")

    print('You may now change the PROGRAM_MODE to "app" or "calibrate"')
