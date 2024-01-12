# This file allows you to play an audio file
# and flash the LEDs at the same time.

import board
import audiomp3
import audiopwmio
import time
import neopixel

NUM_LEDS = 15
LED_PIN = board.GP0
AUDIO_PIN = board.GP16

pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS)
audio = audiopwmio.PWMAudioOut(AUDIO_PIN)
decoder = audiomp3.MP3Decoder(open("juice.mp3", "rb"))

while True:
    # Start playing audio file
    if not audio.playing:
        audio.play(decoder)

    # Flash LEDs simultaneously
    pixels.fill((255, 0, 0))  # Turn the LEDs red
    time.sleep(0.5)
    pixels.fill((0, 0, 0))  # Turn the LEDs off
    time.sleep(0.5)
