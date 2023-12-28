# CircuitPython demo - NeoPixel
import time
import board
import neopixel
import adafruit_dotstar
import touchio


touch_A1 = touchio.TouchIn(board.A1)
touch_A2 = touchio.TouchIn(board.A2)

led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)

pixel_pin = board.A0
num_pixels = 6
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

initial_time = time.monotonic()
blink_speed = .5

def cycle_sequence(seq):
    """Allows other generators to iterate infinitely"""
    while True:
        for elem in seq:
            yield elem

C0 = ((226, 39, 230), (34, 226, 230), (165, 34, 230),(41, 93, 148))  # Harlow Favorite colors
C1 = ((0, 39, 76), (255, 203, 5))  # Michigan Colors
C2 = ((153, 27, 30), (255,199,44))  # USC
C3 = ((255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (139, 0, 255))  # rainbow
C4 = ((204, 0, 0), (0, 102, 0))  # Xman Colors
C5 = ((180, 32, 51), (254, 254, 254), (60, 59, 110)) #USA
C6 = ((138, 98, 6),(254, 254, 254),(212, 8, 19)) #Elf Colors

color_list_initial = C0
touch_A1_state = None
touch_A2_state = None

speeds_list = cycle_sequence([0.15, 0.3, 0.45, .6])
color_list = cycle_sequence([C0, C1, C2, C3,C4,C5,C6])

colors = next(color_list)
wait = next(speeds_list)

while True:

    # for i in range(num_pixels):
    #    pixels[i] = C0

    led.brightness = 0.7

    current_time = time.monotonic()
    for j in range(len(colors)):
        for i in range(num_pixels):
            if current_time >= initial_time+wait*(num_pixels*j+i) and current_time <= initial_time+wait*(num_pixels*j+i+1):
                pixels[i] = colors[j]
                pixels.show()

    if current_time >= initial_time + (len(colors)*num_pixels+1)*wait:
        initial_time = current_time

    if not touch_A1.value and touch_A1_state is None:
        touch_A1_state = "ready"
    if touch_A1.value and touch_A1_state == "ready":
        wait = next(speeds_list)
        # print("Touch 1")
        touch_A1_state = None

    if not touch_A2.value and touch_A2_state is None:
        touch_A2_state = "ready"
    if touch_A2.value and touch_A2_state == "ready":
        colors = next(color_list)
        # print("Touch 2")
        touch_A2_state = None

    # print(touch_A2.raw_value)
