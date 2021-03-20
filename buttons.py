from colors import * 

def XY(x, y, offset=-1):
    return ((y+offset)*8 + (x+offset))

color = OFF

def momentary(color = OFF, off = -1, on = -1): #use to make key momentary
    if on == -1:
        on = color
    if off == -1:
        off = (round(on[0] / 5), round(on[1] / 5), round(on[2] / 5))
    return {'off': off, 'on': on, 'type': 'momentary'}

def latching(color = OFF, off = -1, on = -1): #use to make key latching
    if on == -1:
        on = color
    if off == -1:
        off = (round(on[0] / 5), round(on[1] / 5), round(on[2] / 5))
    return {'off': off, 'on': on, 'state': False, 'type': 'latching'}

# --------------------------------------------------------------------------------------

# BUTTONS - top left = 1,1, bottom-right = 8,8
# 0 = button, 1 = pad data, 2 = midi data (need to change some code around to get this to work)

BUTTONS8x8 = [
    [XY(1, 1), momentary( RED    )],
    [XY(2, 1), momentary( ORANGE )],
    [XY(3, 1), momentary( YELLOW )],
    [XY(4, 1), momentary( GREEN  )],
    [XY(5, 1), momentary( CYAN  )],
    [XY(6, 1), momentary( BLUE   )],
    [XY(7, 1), momentary( PURPLE )],
    [XY(8, 1), momentary( PINK   )],

    [XY(1, 2), momentary( W10 )],
    [XY(2, 2), momentary( W25 )],
    [XY(3, 2), momentary( W40 )],
    [XY(4, 2), momentary( W50 )],
    [XY(5, 2), momentary( W60 )],
    [XY(6, 2), momentary( W75 )],
    [XY(7, 2), momentary( W90 )],
    [XY(8, 2), momentary( W100 )],


    [XY(1, 3), momentary( RED    )],
    [XY(2, 3), momentary( ORANGE )],
    [XY(3, 3), momentary( YELLOW )],
    [XY(4, 3), momentary( GREEN  )],
    [XY(5, 3), momentary( CYAN  )],
    [XY(6, 3), momentary( BLUE   )],
    [XY(7, 3), momentary( PURPLE )],
    [XY(8, 3), momentary( PINK   )],

    [XY(1, 4), momentary( W10 )],
    [XY(2, 4), momentary( W25 )],
    [XY(3, 4), momentary( W40 )],
    [XY(4, 4), momentary( W50 )],
    [XY(5, 4), momentary( W60 )],
    [XY(6, 4), momentary( W75 )],
    [XY(7, 4), momentary( W90 )],
    [XY(8, 4), momentary( W100 )],

    [XY(1, 5), momentary( RED    )],
    [XY(2, 5), momentary( ORANGE )],
    [XY(3, 5), momentary( YELLOW )],
    [XY(4, 5), momentary( GREEN  )],
    [XY(5, 5), momentary( CYAN  )],
    [XY(6, 5), momentary( BLUE   )],
    [XY(7, 5), momentary( PURPLE )],
    [XY(8, 5), momentary( PINK   )],

    [XY(1, 6), momentary( W10 )],
    [XY(2, 6), momentary( W25 )],
    [XY(3, 6), momentary( W40 )],
    [XY(4, 6), momentary( W50 )],
    [XY(5, 6), momentary( W60 )],
    [XY(6, 6), momentary( W75 )],
    [XY(7, 6), momentary( W90 )],
    [XY(8, 6), momentary( W100 )],    

    [XY(1, 7), momentary( RED    )],
    [XY(2, 7), momentary( ORANGE )],
    [XY(3, 7), momentary( YELLOW )],
    [XY(4, 7), momentary( GREEN  )],
    [XY(5, 7), momentary( CYAN  )],
    [XY(6, 7), momentary( BLUE   )],
    [XY(7, 7), momentary( PURPLE )],
    [XY(8, 7), momentary( PINK   )],

    [XY(1, 8), momentary( W10 )],
    [XY(2, 8), momentary( W25 )],
    [XY(3, 8), momentary( W40 )],
    [XY(4, 8), momentary( W50 )],
    [XY(5, 8), momentary( W60 )],
    [XY(6, 8), momentary( W75 )],
    [XY(7, 8), momentary( W90 )],
    [XY(8, 8), momentary( W100 )]
]