from machine import Pin

LED_PIN = 2
RGB_PIN = 22
BUZZER_PIN = 5

led = Pin(LED_PIN, Pin.OUT)
rgb = Pin(RGB_PIN, Pin.OUT)
buzzer = Pin(BUZZER_PIN, Pin.OUT)