import requests
import time
from script_template import *

#scrivere l'exploit qua, ritorna singola flag. info1 e info2 sono i valori recuperati da flagID
def exploit(ip, info1, info2):
    flag = ""
    #exploit qua
    
    return flag

#per mandare attacco, modificare solo service, info1 e info2
def send_attack(ip, team_id):
    print(f"Attacco in corso a {ip}\n")
    service = ""  # servizio
    info1 = ""    # primo argomento flagID
    info2 = ""    # secondo argomento flagID

    results = get_info(team_id, service, info1, info2)  # ritorna una lista di dizionari

    print(results)  # debug opzionale

    for i in range(0, 4):
        if not results[i]:  # check se è vuoto
            continue

        arg1 = results[i][info1]
        arg2 = results[i][info2]

        flag = exploit(ip, arg1, arg2)

        data = {'flag': flag}
        response = requests.post(submitter_ip, data=data)

        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

    return

#funzione per salvare le flag su un file, ma non serve più
def save_flag(flag):
    try:
        with open("CTF-Tools/flags.txt", "a") as f:
            f.write(flag + "\n")
        print(f"Flag salvata: {flag}\n")
        return 1
    except Exception as e:
        print(f"[!] Errore durante il salvataggio della flag: {e}\n")
        return 0

if __name__ == "__main__":
    team_ip = "10.60.64.1"
    teams = 81 #da modificare in base al numero di team
    round_inf = 0 #scrivere qua round minore
    submitter_ip = "http://10.81.64.1:5000" #scrivere qua submitter id
    while True:
        flags_found = 0
        for i in range(teams):
            ip = f"10.60.{i}.1"
            if ip == team_ip:
                continue
            try:
                print(f"Inizio attacco a {ip}")
                flag = send_attack(ip, i)
                if flag:  # Se è stata trovata una flag
                    flags_found += 1
            except Exception as e:
                print(f"[!] Errore durante l'attacco a {ip}: {e}")

        print(f"Giro completato. Trovate {flags_found} flag. Aspetto 120 secondi per il prossimo attacco...\n")
        time.sleep(120)
