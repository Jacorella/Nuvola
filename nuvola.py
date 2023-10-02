import commands
from colorama import init, Fore, Style

init(autoreset=True)

try:
    with open("credenziali.txt", "r") as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
except FileNotFoundError:
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la tua password: ")
    with open("credenziali.txt", "w") as file:
        file.write(username + "\n")
        file.write(password + "\n")

print(Fore.YELLOW + Style.BRIGHT + "Aspetta un momento...")

try:
    csrf_token = commands.get_csrf_token()
    session_token = commands.login(username, password, csrf_token)
    token = commands.get_bearer_token(session_token)
    info_alunno = commands.alunni(token)
except Exception as e:
    print(Fore.RED + f"Si è verificato un errore: {e}")

while True:
    print(Fore.CYAN + "1: Visualizza i Voti")
    print(Fore.CYAN + "2: Visualizza i Compiti")
    choice = input("Inserisci la tua scelta: ")

    if choice == "1":
        commands.visualizza_voti(token)
    elif choice == "2":
        commands.visualizza_compiti(token,giorni=5)
    else:
        print(Fore.RED + "Scelta non valida. Riprova.")
