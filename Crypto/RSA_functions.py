from Crypto.Util.number import inverse
from sympy import factorint
import multiprocessing

class TimeoutException(Exception):
    pass

#Per gestire n troppo elevati
def find_factors_process(n, result_queue):
    try:
        factors = factorint(n)
        expanded = []
        for prime, exponent in factors.items():
            expanded.extend([prime] * exponent)
        result_queue.put(expanded)
    except Exception as e:
        result_queue.put(str(e))

#Ritorna una lista dei numeri primi che compongono n (per n non troppo grande)
#quando invochi la funzione puoi aumentare il timeout se vuoi, altrimenti di default è pari a 10 secondi
def find_factors(n, timeout_seconds=10):
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=find_factors_process, args=(n, result_queue))

    process.start()
    process.join(timeout_seconds)

    if process.is_alive():
        process.terminate()
        return f"Timeout: n troppo grande, operazione interrotta dopo {timeout_seconds} secondi.\nProva a vedere su https://factordb.com/"
    
    return result_queue.get() if not result_queue.empty() else None

def get_n(p, q):
    return p*q

def str_to_bytes(message_str):
    message_bytes = message_str.encode()
    # Calcola il valore decimale del messaggio
    m = int.from_bytes(message_bytes, "big")
    return m

def encrypt(message, e, n):
    c = pow(message, e, n)
    return c

def get_tot(p, q):
    tot_n = (p-1)*(q-1)
    return tot_n

def get_d(e, phi_n):
    d = inverse(e, phi_n)
    return d

def decrypt(c, d, n):
    m = pow(c, d, n)
    return m

#esempio
if __name__ == "__main__":
    n = 275
    a = find_factors(n)
    print(a)