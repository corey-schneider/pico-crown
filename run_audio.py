# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import board
import audiomp3
import audiopwmio
import time

print("Hello World!")

audio = audiopwmio.PWMAudioOut(board.GP0)

decoder = audiomp3.MP3Decoder(open("juice.mp3", "rb"))

while(True):
    audio.play(decoder)
    while audio.playing:
        pass
    print("replaying")
    time.sleep(1)

print("Done playing!")
