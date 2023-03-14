import network
from machine import Pin, ADC

from config import MAX_ADC_VALUE

conversion_factor = 3 * 3.3 / MAX_ADC_VALUE


def get_vsys():
    wlan = network.WLAN(network.STA_IF)
    wlan_active = wlan.active()

    try:
        # Don't use the WLAN chip for a moment.
        wlan.active(False)

        # Make sure pin 25 is high.
        Pin(25, mode=Pin.OUT, pull=Pin.PULL_DOWN).high()

        # Reconfigure pin 29 as an input.
        Pin(29, Pin.IN)

        vsys = ADC(29)
        return vsys.read_u16() * conversion_factor

    finally:
        # Restore the pin state and possibly reactivate WLAN
        Pin(29, Pin.ALT, pull=Pin.PULL_DOWN, alt=7)
        wlan.active(wlan_active)
