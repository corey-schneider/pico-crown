import array
import time
import board
import digitalio
import neopixel
import math

# Configure the number of WS2812 LEDs.
NUM_LEDS = 15
PINOUT = board.GP0
CYCLE_TIME = 1  # in seconds
BRIGHTNESS = 0.3  # Adjust this value to dim or brighten the LEDs

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
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (75, 0, 130),     # Indigo
    (148, 0, 211),    # Violet
    (255, 255, 255)   # White
]

while True:
    for i in range(len(colors_to_cycle) - 1):
        update_smooth_color_transition(colors_to_cycle[i], colors_to_cycle[i + 1], CYCLE_TIME)
    update_smooth_color_transition(colors_to_cycle[-1], colors_to_cycle[0], CYCLE_TIME)

