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

BUTTONS = BUTTONS8x8

trellis = MultiTrellis(trelli)

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
        # print('key press! ', padNum)
        
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
        # print('key release! ', padNum)
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
    sleep(0.01)