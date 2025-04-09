import requests
import time
import json
def extract_round_from_flag(flag):
    try:
        return int(flag[0:2], 36)
    except IndexError:
        return "unknown"

def send_flags():
    TEAM_TOKEN = ''  # Insert your token here
    sent_flags_dict = dict()
    unsent_flags = dict()
    error_counter = 0
    while True:
        if(unsent_flags):
            print(f'Flag non inviate già inserite: {len(unsent_flags)}/500')
        print("Inserisci fino a 500 flag (una per riga). Scrivi 'send' per inviarle subito. Scrivi 'clear' per pulire lista di flag")
        while len(unsent_flags) < 500:
            try:
                line = input().strip()
                #print(len(line))
            except EOFError:
                print("Input terminato.")
                break
            if line.lower() == 'send':
                break
            elif line.lower() == 'clear':
                if unsent_flags:
                    unsent_flags.clear()
                #print(len(unsent_flags)) per debug
                print("Lista di flag non inviate azzerata\n")
                print("Inserisci fino a 500 flag (una per riga). Scrivi 'send' per inviarle subito. Scrivi 'clear' per pulire lista di flag")
            elif line == '':
                continue
            elif line in sent_flags_dict:
                print(f"Flag '{line}' già inviata e accettata (round {sent_flags_dict[line]['round']}, timestamp {sent_flags_dict[line]['timestamp']}).\n")
                continue
            elif line in unsent_flags:
                print(f"Flag '{line}' già inserita in questo ciclo (round {unsent_flags[line]}).\n")
                continue
            elif len(line)!=32:
                print(f"Flag '{line}' non valida.\n")
                continue
            else:
                round_id = extract_round_from_flag(line)
                unsent_flags[line] = round_id
                #print(len(unsent_flags)) debug
                #print(unsent_flags) debug
                print(f"Flag '{line}' aggiunta (round: {round_id}) [{len(unsent_flags)}/500]\n")


        if(error_counter == 5):
            unsent_flags.clear()
        if unsent_flags:
            flags_to_send = list(unsent_flags.keys())
            #Se dà errore nell'invio per 5 volte di seguito pulisce la lista di flag non inviate 
            print(f"\nInvio di {len(flags_to_send)} flag...\n")
            try:
                json_data = json.dumps(flags_to_send)
                # Calcola la dimensione del corpo della richiesta (in byte)
                request_size = len(json_data.encode('utf-8'))  # Utilizza 'utf-8' per ottenere la dimensione in byte
                print(f"Dimensione della richiesta: {request_size} byte")
                response = requests.put('http://10.10.0.1:8080/flags', headers={
                    'X-Team-Token': TEAM_TOKEN
                }, json=flags_to_send)

                print("Risposta del server:", response.text)
                
                if response.status_code == 200:
                    # Assumiamo che la risposta sia una lista di oggetti JSON per ogni flag
                    response_json = response.json()
                    error_counter = 0
                    # Elabora ogni risposta per le flag inviate
                    for res in response_json:
                        flag = res['flag']
                        stato = res['status']
                        messaggio = res.get('msg', '')

                        if stato == "ACCEPTED":
                            # Flag inviata con successo: rimuovila da unsent_flags e aggiungila a sent_flags_dict
                            sent_flags_dict[flag] = {
                                'round': unsent_flags[flag],
                                'timestamp': time.time()
                            }
                            print(f"Flag '{flag}' inviata con successo.")
                            unsent_flags.pop(flag, None)  # Rimuovi la flag da unsent_flags

                        elif stato == "DENIED":
                            if "invalid flag" in messaggio:
                                print(f"Flag '{flag}' è invalida. va rimossa.")
                                unsent_flags.pop(flag, None)  # Rimuovi la flag
                            elif "from nop team" in messaggio:
                                print(f"Flag '{flag}' è della NOP team. Non vale punti, va rimossa.")
                                unsent_flags.pop(flag, None)  # Rimuovi la flag
                            elif "is your own" in messaggio:
                                print(f"Flag '{flag}' è tua. Non vale punti, va rimossa.")
                                unsent_flags.pop(flag, None)  # Rimuovi la flag
                            elif "too old" in messaggio:
                                print(f"Flag '{flag}' è troppo vecchia, va rimossa.")
                                unsent_flags.pop(flag, None)  # Rimuovi la flag
                            elif "already claimed" in messaggio:
                                print(f"Flag '{flag}' è già stata reclamata, va rimossa.")
                                unsent_flags.pop(flag, None)  # Rimuovi la flag
                            elif "dispatch" in messaggio:
                                print(f"Flag '{flag}' non verificata correttamente. Rimane in attesa.")
                                # La flag rimane in attesa senza essere rimossa

                        elif stato == "RESUBMIT":
                            print(f"Flag '{flag}' non attiva ancora. Aspetta il prossimo round.")
                            # La flag non attiva deve restare in unsent_flags
                            # Nessuna modifica da fare, rimane come era

                        elif stato == "ERROR":
                            print(f"Errore con la flag '{flag}'. Ritenta più tardi.")
                            # In caso di errore, conserva la flag per il prossimo tentativo
                            # Nessuna modifica da fare, rimane come era

                    print("Tutte le risposte elaborate.")
                else:
                    print("Invio fallito. Le flag non inviate vengono memorizzate per il prossimo ciclo.")

            except Exception as e:
                print(f"Errore durante l'invio: {e}")
                error_counter += 1

        else:
            print("Nessuna nuova flag da inviare.")

        current_time = time.time()
        for flag, data in list(sent_flags_dict.items()):
            if current_time - data['timestamp'] > 15 * 60:  # 15 minuti
                print(f"Flag '{flag}' è troppo vecchia (inviata più di 15 minuti fa). Rimuoviamo.")
                sent_flags_dict.pop(flag)

        print("\n--- Pronto per il prossimo batch ---\n")

if __name__ == "__main__":
    send_flags()
