![crown](20240112_181939.jpg)

This project utilizes the following devices:
- Raspberry Pi Pico W
- Bottle of Crown Royal
- 2.5w speaker (pulled from an old laptop)
- PAM8302A 2.5w amplifier
- 0.5m of 5v WS2812B RGB LEDs, 15 LEDs total
- Some wood and hot glue

and software:
- MicroPython 8.2.9
- MQTT
- Adafruit IO
- Misc Adafruit libraries
  
to accomplish the following task:
- Allow me to send an alert to the device over the internet in order for it to play a specific noise and flash the LEDs a specific way, both similar and very dissimilar to an alarm clock.

Features:
- On startup:
  - Flash white 2 times to indicate the code is running and the LEDs are communicating
  - Connect to wifi in `settings.toml`
    - If wifi connection fails for any reason, slowly flash red 5x to indicate a wifi error
  - Begin cycling all colors slowly
- If command is received from Adafruit:
  - `led_status_feed` (not working)
    - ON / OFF
    - Not working - cannot think of a valid use case
  - `shotty_time_feed`
    - 0 / 1: begins shotty mode: plays a sound and flashes the LEDs simultaneously
  - `brightness_feed`
    -  0.3 to 1.0: sets the brightness. Default is 0.8. Resets on reboot

Circuit:
![circuit](https://github.com/corey-schneider/pico-crown/assets/35932803/68b45213-672a-45fa-9ec0-e527a0d110cb)
