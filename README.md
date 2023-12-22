This project utilizes the following devices:
- Raspberry Pi Pico W
- Bottle of Crown Royale
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
- [ ] On startup:
  - [ ] Flash white 2 or 3 times to indicate the code is running and the LEDs are communicating
  - [ ] Connect to wifi in `settings.toml`
    - [ ] If wifi connection fails for any reason, flash red 5x to indicate a wifi error
  - [ ] Begin cycling all colors slowly
- [ ] If command is received from Adafruit:
  - [ ] `led_status_feed`
    - [ ] ON / OFF: self explanatory
  - [ ] `shotty_time_feed`
    - [ ] 0 / 1: begins shotty mode: plays a sound and flashes the LEDs
  - [ ] `brightness_feed`
    - [ ] 0.3 to 1.0: sets the brightness. Default is 0.8. Resets on reboot
- [ ] Plays sound `run_audio.py`

TODO:
- [ ] Save brightness_feed value and use it, or default 0.8
- [ ] 

Circuit:
![circuit](https://github.com/corey-schneider/pico-crown/assets/35932803/fe5d0307-3076-488f-9792-9d5ff8ff44d9)
