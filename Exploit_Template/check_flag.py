import re

def check_flag(flag):
    regex_flag = "[A-Z0-9]{31}=$"
    #flag = "080A02AF0J07UMOPHNE00KJ48KAE28C="

    
    if re.fullmatch(regex_flag, flag):
        print("String matches the regex!")
        return 1
    else:
        return 0