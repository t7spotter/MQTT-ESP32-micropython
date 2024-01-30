from machine import Pin
from relays import *

LED_PIN = 2
RGB_PIN = 22
BUZZER_PIN = 5

led = Pin(LED_PIN, Pin.OUT)
rgb = Pin(RGB_PIN, Pin.OUT)
buzzer = Pin(BUZZER_PIN, Pin.OUT)


topics_to_subscribe = {
"MQTT_TOPIC_RELAYS": bytes(f"esp32/relays", "utf-8"),
"MQTT_TOPIC_LED": bytes(f"esp32/led", "utf-8"),
"MQTT_TOPIC_BUZZER": bytes(f"esp32/buzzer", "utf-8"),
"MQTT_TOPIC_RELAY1": bytes(f"esp32/relay1", "utf-8"),
"MQTT_TOPIC_RELAY2": bytes(f"esp32/relay2", "utf-8"),
"MQTT_TOPIC_RELAY3": bytes(f"esp32/relay3", "utf-8"),
"MQTT_TOPIC_RELAY4": bytes(f"esp32/relay4", "utf-8"),
"MQTT_TOPIC_RELAY5": bytes(f"esp32/relay5", "utf-8"),
"MQTT_TOPIC_RELAY6": bytes(f"esp32/relay6", "utf-8"),
"MQTT_TOPIC_RELAY7": bytes(f"esp32/relay7", "utf-8"),
"MQTT_TOPIC_RELAY8": bytes(f"esp32/relay8", "utf-8"),
"MQTT_TOPIC_RGB": bytes(f"esp32/rgb", "utf-8"),
}