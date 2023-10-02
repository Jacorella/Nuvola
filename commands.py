import requests
from bs4 import BeautifulSoup as Bs
from colorama import init, Fore, Style
from datetime import datetime, timedelta

init(autoreset=True)
s = requests.Session()

def get_csrf_token():
    try:
        login_page = s.get("https://nuvola.madisoft.it")
        login_page.raise_for_status() 
        csrf_token = Bs(login_page.text, features="lxml").find_all("input")[0].attrs["value"]
        return csrf_token
    except requests.exceptions.HTTPError as errh:
        print(f"Errore HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Errore di connessione: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout della richiesta: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante la richiesta: {err}")

def login(username, password, csrf_token):
    try:
        r = s.post("https://nuvola.madisoft.it/login_check", data={
            "_username": username,
            "_password": password,
            "_csrf_token": csrf_token
        })
        r.raise_for_status()
        return r.cookies.get("nuvola")
    except requests.exceptions.HTTPError as errh:
        print(f"Errore HTTP durante il login: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante il login: {err}")

def get_bearer_token(session_token):
    try:
        r = s.get("https://nuvola.madisoft.it/api-studente/v1/login-from-web", cookies={"nuvola": session_token})
        r.raise_for_status()
        token = r.json()["token"]
        return token
    except requests.exceptions.HTTPError as errh:
        print(f"Errore HTTP durante l'ottenimento del bearer token: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante l'ottenimento del bearer token: {err}")
        

def visualizza_voti(token):
    print(Fore.CYAN  + "1. Primo Quadrimestre")
    print(Fore.CYAN + "2. Secondo Quadrimestre")
    print(Fore.CYAN + "3. Intero Anno")
    choice = input("Inserisci un " + Fore.YELLOW + "numero: " + Fore.RESET)
    if choice == "1":
        id = "7"
    elif choice == "2":
        id = "8"
    elif choice == "3":
        id = "9"
    else:
        print(Fore.RED + "Qualcosa è andato storto")                
    url = f"https://nuvola.madisoft.it/api-studente/v1/alunno/{studente_id}/frazione-temporale/{id}/voti/materie"
    headers = {
        "authorization": "Bearer " + token
    }
    
    r = requests.get(url, headers=headers)
    voti_data = r.json()
    
    for materia in voti_data["valori"]:
        nome_materia = materia["materia"]
        voti = materia["voti"]
        
        if not voti:
            print(Fore.LIGHTMAGENTA_EX + nome_materia + Fore.RESET + ": Nessun Voto")
        else:
            print(Fore.GREEN + nome_materia + ":")
            for voto in voti:
                print(Fore.CYAN + "Voto: " + str(voto))

def alunni(token):
    try:
        headers = {"authorization": "Bearer " + token}
        r = requests.get("https://nuvola.madisoft.it/api-studente/v1/alunni", headers=headers)
        r.raise_for_status()
        info_alunno = r.json()

        for studente in info_alunno["valori"]:
            nome = studente["nome"]
            cognome = studente["cognome"]
            classe = studente["classe"]
            anno_scolastico = str(studente["annoScolastico"])
            global studente_id
            studente_id = str(studente["id"])
            print(Fore.YELLOW + nome + " " + cognome + " " + classe + " " + str(anno_scolastico))
            
    except requests.exceptions.HTTPError as errh:
        print(Fore.RED + f"Errore HTTP durante l'ottenimento dei dati degli alunni: {errh}")
    except requests.exceptions.RequestException as err:
        print(Fore.RED + f"Errore durante l'ottenimento dei dati degli alunni: {err}")
        
def visualizza_compiti(token, giorni=5):
    oggi = datetime.now()

    for giorno in range(giorni):
        data = (oggi + timedelta(days=giorno)).strftime("%d-%m-%Y")
        url = f"https://nuvola.madisoft.it/api-studente/v1/alunno/{studente_id}/compito/elenco/{data}"
        headers = {
            "authorization": "Bearer " + token
        }

        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            compiti_data = r.json()

            for compito in compiti_data["valori"]:
                materia = compito["materia"]
                descrizione_compito = compito["descrizioneCompito"][0] if compito["descrizioneCompito"] else "Niente Compiti"
                
                print(Fore.YELLOW + f"{materia} - Compiti: " + Fore.CYAN + Style.BRIGHT + descrizione_compito + f" | Data: {data}")
                print(Fore.CYAN + "-" * 40)

        except requests.exceptions.HTTPError as errh:
            print(f"Errore HTTP durante il recupero dei compiti: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"Errore durante il recupero dei compiti: {err}")     