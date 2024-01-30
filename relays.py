from machine import Pin

RELAY1_PIN = 13
RELAY2_PIN = 15
RELAY3_PIN = 14
RELAY4_PIN = 27
RELAY5_PIN = 26
RELAY6_PIN = 25
RELAY7_PIN = 18
RELAY8_PIN = 19

relay1 = Pin(RELAY1_PIN, Pin.OUT)
relay2 = Pin(RELAY2_PIN, Pin.OUT)
relay3 = Pin(RELAY3_PIN, Pin.OUT)
relay4 = Pin(RELAY4_PIN, Pin.OUT)
relay5 = Pin(RELAY5_PIN, Pin.OUT)
relay6 = Pin(RELAY6_PIN, Pin.OUT)
relay7 = Pin(RELAY7_PIN, Pin.OUT)
relay8 = Pin(RELAY8_PIN, Pin.OUT)

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
