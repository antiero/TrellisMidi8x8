import time
from time import sleep
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

from buttons import *

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

"""create the trellis. This is for a 2x2 array of NeoTrellis boards
for a 2x1 array (2 boards connected left to right) you would use:
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x2F)]
    ]
"""
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x2F)],
    [NeoTrellis(i2c_bus, False, addr=0x30), NeoTrellis(i2c_bus, False, addr=0x31)],
]

tempo = 60  # Starting BPM
 
# You can use the accelerometer to speed/slow down tempo by tilting!
ENABLE_TILT_TEMPO = True
MIN_TEMPO = 100
MAX_TEMPO = 300

BUTTONS = BUTTONS8x8

trellis = MultiTrellis(trelli)

# pressed_keys - A list of tuples of currently pressed button coordinates
trellis.pressed_keys = set()

# currently pressed sequencer buttons
current_press = set()

# Our global state
current_step = 7 # we actually start on the last step since we increment first
# the state of the sequencer
beatset = [[False] * 8,
           [False] * 8,
           [False] * 8,
           [False] * 8,
           [False] * 8,
           [False] * 8,
           [False] * 8,
           [False] * 8]

# light up all keys at start
for y in range(8):
	for x in range(8):
		trellis.color(y, x, 0x020202)
		sleep(0.01)

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# --------------------------------------------------------------------------------------

buttonData = [{}, {}]  # [{key nums: data}, {key nums: midi data}]
keys = [] # [keynum] -> [1 = key data [momentary, latching]], [2 = midi data (int or tuple)]

for button in BUTTONS:
    buttonData[0].update({button[0]: button[1]})  # add key data
    #buttonData[1].update({button[0]: button[2]})  # add midi data

for keynum in range(0, 64):
    stuff = [
        keynum,
        buttonData[0].get(keynum, {'off': OFF, 'on': OFF, 'type': 'empty'}),
        buttonData[1].get(keynum, 0)
    ]

    keys.append(stuff)

# --------------------------------------------------------------------------------------

def blink(xcoord, ycoord, edge):
    padNum = XY(xcoord, ycoord, 0)

    if edge == NeoTrellis.EDGE_RISING:
        print('key press! ', padNum)
        trellis.pressed_keys.add((xcoord,ycoord))
        
        if keys[padNum][1]['type'] is 'momentary':
            #print('momentary ', padNum, ' on')
            #midi.send(NoteOn(keys[padNum][2], 120))
            midi.send(NoteOn(padNum))

            color = keys[padNum][1]['on']
            trellis.color(xcoord, ycoord, color)

        elif keys[padNum][1]['type'] is 'latching':
            #midi.send(NoteOn(keys[padNum][2], 120))
            midi.send(NoteOn(padNum))

            if not keys[padNum][1]['state']:
                color = keys[padNum][1]['on']
                #print('latching ', padNum, ' on ', keys[padNum])

            elif keys[padNum][1]['state']:
                color = keys[padNum][1]['off']
                #print('latching ', padNum, ' off ', keys[padNum])

            trellis.color(xcoord, ycoord, color)
            keys[padNum][1]['state'] = not keys[padNum][1]['state']

    elif edge == NeoTrellis.EDGE_FALLING:
        print('key release! ', padNum)
        if (xcoord,ycoord) in current_press:
            trellis.pressed_keys.remove((xcoord,ycoord))
        if keys[padNum][1]['type'] is 'momentary':
            #print('momentary ', padNum, ' off')
            midi.send(NoteOff(padNum))
            color = keys[padNum][1]['off']
            trellis.color(xcoord, ycoord, color)

# turn off all keys now. this way you can tell if anything errored between line 32 and here
for y in range(8):
    for x in range(8):
        trellis.color(x, y, keys[XY(x, y, 0)][1]['off'])
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, blink)
        sleep(0.01)

while True:
    trellis.sync()
    
    stamp = time.monotonic()
    # redraw the last step to remove the ticker bar (e.g. 'normal' view)
    for y in range(8):
        color = 0
        if beatset[y][current_step]:
            color = DRUM_COLOR[y]
        trellis.color(current_step, y, color)
 
    # next beat!
    current_step = (current_step + 1) % 8
 
    # draw the vertical ticker bar, with selected voices highlighted
    for y in range(8):
        if beatset[y][current_step]:
            r, g, b = DRUM_COLOR[y]
            color = (r//2, g//2, b//2)  # this voice is enabled
            print("Playing: ", VOICES[y])
            #mixer.play(samples[y], voice=y)
        else:
            color = TICKER_COLOR     # no voice on
        trellis.color(current_step, y, color)
 
    # handle button presses while we're waiting for the next tempo beat
    while time.monotonic() - stamp < 60.0/(tempo/0.125):
        # Check for pressed buttons
        pressed = trellis.pressed_keys
        #print(pressed)
        for down in pressed - current_press:
            print("Pressed down", down)
            y = down[0]
            x = down[1]
            beatset[y][x] = not beatset[y][x] # enable the voice
            if beatset[y][x]:
                color = DRUM_COLOR[y]
            else:
                color = 0
            trellis.color(x, y, color)
        current_press = pressed
    
    sleep(0.01)