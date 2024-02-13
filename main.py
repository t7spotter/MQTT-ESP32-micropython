import urequests
import network
import gc
import _thread
from machine import Pin, Timer
from neopixel import NeoPixel
from umqtt.simple import MQTTClient
from time import sleep
import time
from relays import *
from pins import Pins
from enviorments import (
    CHAT_ID,
    
    WIFI_SSID,
    WIFI_PASSWORD,
    
    BROKER_PORT,
)

timer = Timer(0)

led = Pin(Pins.LED_PIN, Pin.OUT)
rgb = Pin(Pins.RGB_PIN, Pin.OUT)
buzzer = Pin(Pins.BUZZER_PIN, Pin.OUT)


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

def send_telegram_message(message):
            url = "telegramapi.org" # add ypur telegram API endpoint
            payload = {
                # "bot_token": BOT_TOKEN,
                "chat_id": CHAT_ID,
                "message": message,
            }
            response = urequests.post(url, json=payload)
            return response

def toggle_en_pin(gpio_pin):
        """ It's push the EN (board reboot) button """
        en_pin = Pin(gpio_pin, Pin.OUT)
        en_pin.value(1)
        time.sleep(0.1)
        en_pin.value(0)
        
def blink(number_of_blinkings):
    led = Pin(Pins.LED_PIN, Pin.OUT)
    for _ in range(number_of_blinkings):
        led.on()
        sleep(0.15)
        led.off()
        sleep(0.15)
        
def neo_pixel(pin, R, G, B):
    np = NeoPixel(Pin(pin), 1)
    np[0] = (R, G, B)
    return np.write()

def rgb_string_to_rgb(rgb_string):
    try:
        # Extract numerical values from the RGB string
        rgb_values_str = rgb_string[3:-1].split(',')
        rgb_values = []

        for value_str in rgb_values_str:
            # Remove non-numeric characters and convert to integer
            value = int(''.join(filter(str.isdigit, value_str.strip())))
            value = max(0, min(value, 255))
            rgb_values.append(value)

        # If only two values are provided, assume the third as 0 (e.g., "rgb(0, 255, 191)")
        while len(rgb_values) < 3:
            rgb_values.append(0)

        return tuple(rgb_values)

    except Exception as e:
        print(f"Error parsing RGB string: {e}, Input: {rgb_string}")
        raise ValueError("Error processing RGB values")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
def connect_wifi():
    
    global wlan

    tries = 0
    while not wlan.isconnected():
        try:
            if not wlan.isconnected():
                wlan.connect(WIFI_SSID, WIFI_PASSWORD)
                print(f"\nTrying to connect {WIFI_SSID} Wi-Fi...")
                tries += 1
                sleep(5)
                
            if wlan.isconnected():
                print(f"Connected to the {WIFI_SSID} Wi-Fi after {tries} tries")
                sleep(0.1)
                send_telegram_message(f"Connected to the {WIFI_SSID} Wi-Fi after {tries} tries")
                blink(3)
                
                sleep(0.1)
                
                return wlan
            
        except Exception as e:
            tries += 1
            print(f"Error connecting to Wi-Fi: {e} \nReconnecting to Wi-Fi...")
            time.sleep(20)
            
def connect_mqtt():
    print("Connecting to broker...")
    send_telegram_message(("Connecting to broker..."))
    sleep(0.5)
    mqtt_client = MQTTClient("client_id1", "test.mosquitto.org", port=BROKER_PORT) # Add your own
    mqtt_client.set_callback(on_message)
    mqtt_client.connect()
    sleep(0.5)
    
    for topic in topics_to_subscribe:
        mqtt_client.subscribe(topics_to_subscribe[topic])
    
    gc.collect()
    sleep(0.5)
    blink(4)
    sleep(0.1)

    print("Connected to MQTT broker")
    send_telegram_message("Connected to MQTT broker")
    neo_pixel(22, 100, 200, 0)
    sleep(0.5)
    return mqtt_client

def publish_mqtt_message(my_message, my_topic):
    # MQTT Broker settings
    broker_address = "test.mosquitto.org" # MQTT broker address
    client_id = "client@test" # MQTT client id
    port = 1883 # MQTT port number

    topic = my_topic
    message = my_message

    try:
        # Connect to the MQTT broker
        client = MQTTClient(client_id, broker_address, port)
        client.connect()

        # Publish the message to the specified topic
        client.publish(topic, message)

    except Exception as e:
        print("Error:", e)

    finally:
        # Disconnect from the MQTT broker, even if an exception occurs
        try:
            client.disconnect()
        except:
            pass

def remind_task(timer):
    publish_mqtt_message(b"remind", topics_to_subscribe["MQTT_TOPIC_REMIND"])
    print("Reminded")
    blink(2)


# -------------- MANUAL RELAYS CONTROLL -------------- #
relay1_state = 0
relay2_state = 0
relay3_state = 0
relay4_state = 0

button1 = Pin(Pins.BUTTON_PIN_2, Pin.IN, Pin.PULL_UP)
button2 = Pin(Pins.BUTTON_PIN_4, Pin.IN, Pin.PULL_UP)
button3 = Pin(Pins.BUTTON_PIN_3, Pin.IN, Pin.PULL_UP)
button4 = Pin(Pins.BUTTON_PIN_1, Pin.IN, Pin.PULL_UP)

def manual_relays_toggle():
    global relay1_state, relay2_state, relay3_state, relay4_state, button4
    while True:
        button_state_1 = button1.value()
        button_state_2 = button2.value()
        button_state_3 = button3.value()
        button_state_4 = button4.value()

        if button_state_1 == 0:
            relay1_state = 1 - relay1_state
            relay1.value(relay1_state)
            if relay1_state == 1:
                current_topics_status["RELAY1"] = "m on"
            elif relay1_state == 0:
                current_topics_status["RELAY1"] = "m off"
        
        elif button_state_2 == 0:
            relay2_state = 1 - relay2_state
            relay2.value(relay2_state)
            if relay2_state == 1:
                current_topics_status["RELAY2"] = "m on"
            elif relay2_state == 0:
                current_topics_status["RELAY2"] = "m off"            
        
        elif button_state_3 == 0:
            relay3_state = 1 - relay3_state
            relay3.value(relay3_state)
            if relay3_state == 1:
                current_topics_status["RELAY3"] = "m on"
            elif relay3_state == 0:
                current_topics_status["RELAY3"] = "m off"

        elif button_state_4 == 0:
            relay4_state = 1 - relay4_state
            relay4.value(relay4_state)
            if relay4_state == 1:
                current_topics_status["RELAY4"] = "m on"
            elif relay4_state == 0:
                current_topics_status["RELAY4"] = "m off"
                
        sleep(0.3)
         
current_topics_status = {}
def on_message(topic, msg):
    try:
        print(f"- New message\n- topic: {topic}\n- message: {msg}")
        gc.collect()
        
        if topic == topics_to_subscribe["MQTT_TOPIC_LED"]:
            if msg == b"on":
                led.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                led.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["LED"] = msg
            
        elif topic == topics_to_subscribe["MQTT_TOPIC_BUZZER"]:
            if msg == b"on":
                buzzer.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                buzzer.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["BUZZER"] = msg
        
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAYS"]:
            if msg == b"on":
                all_relays(True)
                sleep(0.1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                all_relays(False)
                sleep(0.1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY1"] = msg
            current_topics_status["RELAY2"] = msg
            current_topics_status["RELAY3"] = msg
            current_topics_status["RELAY4"] = msg
            current_topics_status["RELAY5"] = msg
            current_topics_status["RELAY6"] = msg
            current_topics_status["RELAY7"] = msg
            current_topics_status["RELAY8"] = msg
            
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY1"]:
            if msg == b"on":
                relay1.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay1.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY1"] = msg
            
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY2"]:
            if msg == b"on":
                relay2.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay2.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY2"] = msg
                
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY3"]:
            if msg == b"on":
                relay3.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay3.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY3"] = msg
            
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY4"]:
            if msg == b"on":
                relay4.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay4.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY4"] = msg
            
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY5"]:
            if msg == b"on":
                relay5.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay5.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY5"] = msg

        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY6"]:
            if msg == b"on":
                relay6.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay6.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY6"] = msg
            
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY7"]:
            if msg == b"on":
                relay7.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay7.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY7"] = msg
    
        elif topic == topics_to_subscribe["MQTT_TOPIC_RELAY8"]:
            if msg == b"on":
                relay8.value(1)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            elif msg == b"off":
                relay8.value(0)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: {msg}")
            current_topics_status["RELAY8"] = msg
            
        elif topic == topics_to_subscribe["MQTT_TOPIC_RGB"]:
            try:
                # Convert the RGB message to RGB values
                rgb_values = rgb_string_to_rgb(msg.decode())
                neo_pixel(Pins.RGB_PIN, *rgb_values)
                send_telegram_message(f"- New message\n- topic: {topic}\n- message: LED color set to:\n- R:{rgb_values[0]}\n- G:{rgb_values[1]}\n- B:{rgb_values[2]}")
            except ValueError as e:
                print(f"Error processing RGB values: {e}")
    except Exception as e:
        send_telegram_message(f"Error: unexpected message! {msg} {e}")
        sleep(1)
        print(f"- unexpected message! {msg} {e}")
        

neo_pixel(Pins.RGB_PIN, 0, 0, 0)

# Connect to Wi-Fi
wifi = connect_wifi()
sleep(0.5)

if wlan.isconnected():
    mqtt = connect_mqtt()
    sleep(0.2)
    
    REMIND_IN_MS = int(4.53 * 60 * 1000)    # miliseconds
    timer.init(mode=Timer.PERIODIC, period=REMIND_IN_MS, callback=remind_task)
    
# main loop
while True:
    try:
        if mqtt is not None:
            mqtt.wait_msg()
        else:
            pass

    except Exception as e:
        sleep(0.2)
        if "[Errno 104] ECONNRESET" in e:
            sleep(0.2)
            print(f"{e} triggered\nGPIO reset ...")
            send_telegram_message(f"{e} triggered\nGPIO reset ...")
            sleep(0.5)
            toggle_en_pin(Pins.EN_RESTART_PIN)
        else:
            sleep(0.1)
            neo_pixel(22, 0, 0, 0)
            sleep(0.1)
            gc.collect()
            sleep(1)
            print(f"- Error checking MQTT messages: {e}")
            send_telegram_message(f"- Error checking MQTT messages: {e}")
            sleep(0.25)
            print("reconnecting to broker...")
            send_telegram_message("reconnecting to broker...")
            while not mqtt:
                try:
                    mqtt = connect_mqtt()
                except Exception as e:
                    print(f"213000 handling:\n {e}")
                    send_telegram_message(f"213000 handling:\n{e}") 
    except:
        toggle_en_pin(Pins.EN_RESTART_PIN)