import winsound
import time

def play_error_sound():
    star_wars = [
            (440, 500), (440, 500), (440, 500), (349, 350), (523, 150),
            (440, 500), (349, 350), (523, 150), (440, 1000),             
            (659, 500), (659, 500), (659, 500), (698, 350), (523, 150),  
            (415, 500), (349, 350), (523, 150), (440, 1000)
        ]
    for freq, dur in star_wars:
            winsound.Beep(freq, dur)
            time.sleep(0.05)

def play_good_sound():
    twinkle = [
        (261, 400), (261, 400), (392, 400), (392, 400), # C4, C4, D4, D4
        (440, 400), (440, 400), (392, 800), # E4, E4, D4
        (349, 400), (349, 400), (330, 400), (330, 400), # G4, G4, F4, F4
        (294, 400), (294, 400), (261, 800)  # C4, C4, C4
    ]
    for freq, dur in twinkle:
            winsound.Beep(freq, dur)
            time.sleep(0.05)
