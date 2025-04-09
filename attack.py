import requests
import time

def send_attack(ip):
    print(f"Attacco in corso a {ip}\n")  # per debug
    
    # Simuliamo una flag trovata
    # In un vero attacco, dovresti qui fare una richiesta, leggere una risposta, etc.
    #flag = "flag_example"  # Questa è solo una simulazione
    #print(f"Flag trovata: {flag}")  # Debug per vedere cosa viene restituito
    flag = str(ip)

    return flag

def dec_to_base36(n):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        n, r = divmod(n, 36)
        result = chars[r] + result
    return result

def save_flag(flag):
    try:
        with open("CTF/flags.txt", "a") as f:
            f.write(flag + "\n")
        print(f"Flag salvata: {flag}\n")
    except Exception as e:
        print(f"[!] Errore durante il salvataggio della flag: {e}\n")

if __name__ == "__main__":
    team_ip = ""
    teams = 50 #da modificare in base al numero di team
    while True:
        flags_found = 0
        for i in range(teams):
            base36 = dec_to_base36(i).zfill(2)  # Pad con zero se necessario
            ip = f"10.60.{base36}.1"
            if ip == team_ip:
                continue
            try:
                print(f"Inizio attacco a {ip}")
                flag = send_attack(ip)
                if flag:  # Se è stata trovata una flag
                    save_flag(flag)  # Scrive la flag nel file
                    flags_found += 1
            except Exception as e:
                print(f"[!] Errore durante l'attacco a {ip}: {e}")

        # Aggiungi una riga vuota per separare i round
        with open("CTF/flags.txt", "a") as f:
            f.write("\n\n")

        print(f"Giro completato. Trovate {flags_found} flag. Aspetto 120 secondi per il prossimo attacco...\n")
        time.sleep(120)
