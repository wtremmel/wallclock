# Wallclock

## Preface
This is my very first Python project. So be patient with my code please.
Purpose is to create a wall clock using a 64x64 LED panel with a Raspberry Pi. First idea was to use a RasPi Zero W but it seems it is not fast enough, so currently I am using a RasPi3.

## Hardware
- Raspberry PI. My original idea was to use a Zero W, but the display was flickering with it so I used a 3 I had laying around
- Adafruit RGB bonnet: https://www.adafruit.com/product/3211
- 64x64 RGB LED panel. Ordered here: https://www.aliexpress.com/item/32669762392.html
- 5V 4A power supply.
- 3D printed case for wall mount or desk stand. See directory 3d-files

## Libraries
- Raspi RGB LED Matrix: https://github.com/hzeller/rpi-rgb-led-matrix 
  - I am also using the fonts coming with this library 
- Some Python3 libraries:
  - Astral
  - Pillow
  - Paho Mqtt client


## Structure
I decied to create widget modules for each item I want to display. Feel free to add, fork etc. Also all modules are written for *my* use case. And some of them have the config right in the code (no passworrds though). 

### DateWidget
Displays todays date

### TimeWidget
Displays hours and minutes of the local time

### Secondswidget
A LED bar growing to the right, one LED per second

### TemperatureWidget
A temperature received my MQTT messages. Displays for me the temperature in my garden. Color of temperature changes.


