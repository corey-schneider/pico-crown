import os, ssl, socketpool, wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board, time, neopixel
import array, math, digitalio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 15
PINOUT = board.GP0
CYCLE_TIME = 1  # in seconds
BRIGHTNESS = 0.8  # Adjust this value to dim or brighten the LEDs

pixels = neopixel.NeoPixel(PINOUT, NUM_LEDS, brightness=BRIGHTNESS)

# Display a pattern on the LEDs via an array of LED RGB values.
pixel_array = [0] * NUM_LEDS

# Function to smoothly transition between colors
def interpolate_color(color1, color2, factor):
    r = int(color1[0] + factor * (color2[0] - color1[0]))
    g = int(color1[1] + factor * (color2[1] - color1[1]))
    b = int(color1[2] + factor * (color2[2] - color1[2]))
    return (r, g, b)

# Function to update pixel colors with smooth transitions
def update_smooth_color_transition(color1, color2, duration, steps=100):
    for step in range(steps):
        factor = step / steps
        interpolated_color = interpolate_color(color1, color2, math.sin(math.pi / 2 * factor))
        set_led_color(interpolated_color)
        updatePixel()
        time.sleep(duration / steps)

# Function to set LED colors
def set_led_color(color):
    for i in range(NUM_LEDS):
        pixel_array[i] = (color[1] << 16) + (color[0] << 8) + color[2]

# Function to update the Neopixel strip with new colors
def updatePixel():
    for i in range(NUM_LEDS):
        r = int(((pixel_array[i] >> 8) & 0xFF) * BRIGHTNESS)
        g = int(((pixel_array[i] >> 16) & 0xFF) * BRIGHTNESS)
        b = int((pixel_array[i] & 0xFF) * BRIGHTNESS)
        pixels[i] = (r, g, b)

# Colors to cycle through
colors_to_cycle = [
    (255, 0, 0),      # Red
    #(255, 165, 0),    # Orange
    #(255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    #(75, 0, 130),     # Indigo
    #(148, 0, 211),    # Violet
    #(255, 255, 255)   # White
]
BLACK = (0, 0, 0)

def flash_white():
    for _ in range(3):
        pixels.fill((255, 255, 255))
        time.sleep(0.5)  # Adjust the sleep duration for the desired frequency
        pixels.fill(BLACK)
        time.sleep(0.5)

# Connect to Wifi
#print(f"Connecting to wifi")
#wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
#print("Connected!")

#pool = socketpool.SocketPool(wifi.radio)

aio_username = os.getenv('AIO_USERNAME')
aio_key = os.getenv('AIO_KEY')

led_status_feed = aio_username + "/feeds/led_status"
brightness_feed = aio_username + "/feeds/brightness"
shotty_time_feed = aio_username + "/feeds/shotty_time"

def connected(client, userdata, flags, rc):
    print("Connected to Adafruit IO! Listening for changes.")
    client.subscribe(led_status_feed)
    client.subscribe(shotty_time_feed)
    client.subscribe(brightness_feed)
        
def disconnected(client, userdata, rc):
    print("Disconnected from Adafruit IO.")

# Function to flash the Neopixel strip with a given color and frequency
def flash_color(color, frequency, num_flashes):
    for _ in range(num_flashes):
        pixels.fill(color)
        time.sleep(1 / (2 * frequency))
        pixels.fill(BLACK)
        time.sleep(1 / (2 * frequency))

def cycle_colors():
    for i in range(len(colors_to_cycle) - 1):
        update_smooth_color_transition(colors_to_cycle[i], colors_to_cycle[i + 1], CYCLE_TIME)
    update_smooth_color_transition(colors_to_cycle[-1], colors_to_cycle[0], CYCLE_TIME)
        
def connect_to_wifi():
    try:
        flash_color((255, 255, 255), frequency=3, num_flashes=2) # Flash white 2x on startup
        print("Connecting to wifi")
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
        print("Connected!")
        return True
    except Exception as e:
        print(f"WiFi connection error: {e}")
        return False
    finally:
        pixels.fill(BLACK)

mqtt_client = None

def message(client, topic, message):
    global BRIGHTNESS
    print(f"topic: {topic}, message: {message}")
    if topic == led_status_feed:
        if message == "ON":
            cycle_colors()
        elif message == "OFF":
            pixels.fill(BLACK)
    elif topic == shotty_time_feed:
        if message == "1":
            print("shotty time!")
            flash_color((255, 0, 0), frequency=2, num_flashes=30)
    elif topic == brightness_feed:
        brightness_value = int(message) / 10
        print(f"brightness: {brightness_value}")
        BRIGHTNESS = brightness_value
        # Optionally, you can also update the Neopixel brightness here
        pixels.brightness = BRIGHTNESS
        updatePixel()


if connect_to_wifi():
    pool = socketpool.SocketPool(wifi.radio)
    print("Connecting to Adafruit IO...")
    mqtt_client = MQTT.MQTT(
        broker = os.getenv("BROKER"),
        port = os.getenv("PORT"),
        username = aio_username,
        password = aio_key,
        socket_pool = pool,
        ssl_context = ssl.create_default_context(),
    )

    mqtt_client.on_connect = connected
    mqtt_client.on_disconnect = disconnected
    mqtt_client.on_message = message
    mqtt_client.connect()
else:
    # Handle incorrect WiFi credentials
    print("WiFi connection failed. Flashing red.")
    flash_color((255, 0, 0), frequency=1, num_flashes=5) # Flash red
    print("Cycling through colors.")

while True:
    if mqtt_client is not None:
        mqtt_client.loop()
    print("exited loop, cycling colors...")
    cycle_colors()
    # If any other non-mqtt code, run it in here
