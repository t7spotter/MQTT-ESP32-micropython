from machine import Pin
from pins import Pins

relay1 = Pin(Pins.RELAY1_PIN, Pin.OUT)
relay2 = Pin(Pins.RELAY2_PIN, Pin.OUT)
relay3 = Pin(Pins.RELAY3_PIN, Pin.OUT)
relay4 = Pin(Pins.RELAY4_PIN, Pin.OUT)
relay5 = Pin(Pins.RELAY5_PIN, Pin.OUT)
relay6 = Pin(Pins.RELAY6_PIN, Pin.OUT)
relay7 = Pin(Pins.RELAY7_PIN, Pin.OUT)
relay8 = Pin(Pins.RELAY8_PIN, Pin.OUT)

realys = [
    relay1,
    relay2,
    relay3,
    relay4,
    relay5,
    relay6,
    relay7,
    relay8,
]


def all_relays(status: bool):
    for relay in realys:
        if status is True:
            relay.value(1)
        elif status is False:
            relay.value(0)
