from Exploit_Template.sender import *

flag = "080A02AF0J07UMOPHNE00KJ48KAE28C="
if send_single_flag(flag,"bulk_sender","unknown_bulk","http://10.25.250.26:5000/api/submit"):
    print("DAJE")