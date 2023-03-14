import time

import network
import ntptime
import rp2
from machine import Timer


def wait_for_wifi(wlan):
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1)
    return wlan.status()


def connect(ssid: str, password: str, country: str):
    print(f"Connecting to {ssid}", end=".")
    rp2.country(country)
    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)
    wlan.connect(ssid, password)

    while wait_for_wifi(wlan) != 3:
        print(end=".")
        time.sleep(1)

    print(f" Connected!")

    ifconfig = wlan.ifconfig()
    print(f"IP address is {ifconfig[0]}")

    print(f"Syncing time… ", end="")
    time.sleep(2)
    ntptime.settime()
    print(f"OK {time.localtime()}")


def connect_blink(led, ssid: str, password: str, country: str):
    timer = Timer()

    timer.init(freq=8, mode=Timer.PERIODIC, callback=lambda x: led.toggle())
    connect(ssid, password, country)
    timer.deinit()
    led.off()
