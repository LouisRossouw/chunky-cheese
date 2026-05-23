"""
Techno animation - exciting and fast-paced, ~10 seconds
"""

animation = []
total_duration = 0.0
target_duration = 10.0

cyan = (0, 255, 255)
magenta = (255, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

def add_frame(c1, c2, c3, dur):
    global total_duration
    animation.append({"colors": [c1, c2, c3], "duration": dur})
    total_duration += dur

def seq_strobe(color, times, dur=0.03):
    for _ in range(times):
        add_frame(color, color, color, dur)
        add_frame(black, black, black, dur)

def seq_chase(color, dur=0.05):
    add_frame(color, black, black, dur)
    add_frame(black, color, black, dur)
    add_frame(black, black, color, dur)

def seq_bounce(c1, c2, dur=0.05):
    add_frame(c1, black, c1, dur)
    add_frame(black, c2, black, dur)
    add_frame(c1, black, c1, dur)
    add_frame(black, c2, black, dur)

while total_duration < target_duration:
    # Build up: chase and strobe
    for _ in range(4):
        seq_chase(cyan, 0.04)
    seq_strobe(white, 4, 0.03)
    
    for _ in range(4):
        seq_chase(magenta, 0.04)
    seq_strobe(white, 4, 0.03)
    
    # Bounce section (offbeats)
    for _ in range(4):
        seq_bounce(yellow, blue, 0.06)
        seq_strobe(red, 2, 0.03)

    # Fast alternating strobe
    for _ in range(8):
        add_frame(magenta, cyan, magenta, 0.05)
        add_frame(cyan, magenta, cyan, 0.05)
        
    # Bass drop
    add_frame(white, white, white, 0.1)
    add_frame(black, black, black, 0.15)
    add_frame(green, green, green, 0.1)
    add_frame(black, black, black, 0.15)

# Ensure LEDs are off at the end
add_frame(black, black, black, 0.0)

# clean up namespace so we just export animation
del total_duration
del target_duration
del cyan
del magenta
del yellow
del white
del black
del green
del blue
del red
del add_frame
del seq_strobe
del seq_chase
del seq_bounce
