from machine import unique_id
import ubinascii

# Get the device id
device_id = ubinascii.hexlify(unique_id()).decode("utf-8")
