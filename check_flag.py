import re
from play_sound import *

def check_flag(flag):
    regex_flag = "[A-Z0-9]{31}=$"
    #flag = "080A02AF0J07UMOPHNE00KJ48KAE28C="

    star_wars = [
        (440, 500), (440, 500), (440, 500), (349, 350), (523, 150),
        (440, 500), (349, 350), (523, 150), (440, 1000),             
        (659, 500), (659, 500), (659, 500), (698, 350), (523, 150),  
        (415, 500), (349, 350), (523, 150), (440, 1000)
    ]


    twinkle = [
        (261, 400), (261, 400), (392, 400), (392, 400), # C4, C4, D4, D4
        (440, 400), (440, 400), (392, 800), # E4, E4, D4
        (349, 400), (349, 400), (330, 400), (330, 400), # G4, G4, F4, F4
        (294, 400), (294, 400), (261, 800)  # C4, C4, C4
    ]

    if re.fullmatch(regex_flag, flag):
        print("String matches the regex!")
        play_good_sound()
        return 1
    else:
        play_error_sound()
        return 0