import socket 
from _thread import *
from datetime import datetime

#per killare il processo in caso di errori: fuser -k 4444/tcp

logging=False # stampa chatlog su file
debug=False # stampa chatlog su terminale
host="localhost"
port=4444    
MAX_CONNECTIONS=30

if logging:
    path="log_"+str(datetime.now())[:-7]+".txt"
    log=open("log_"+str(datetime.now())[:-7]+".txt", "w")
    log.close()
    
logged_usernames=[]
users={}
logged_users=0

def client_handler(connection, address):
    global logged_users
    logged_users+=1
    welcome_message=">Seleziona un username per iniziare a comunicare (massimo 20 caratteri):\n"
    connection.sendall(welcome_message.encode())
    username=connection.recv(1024).rstrip().decode()

    if len(username)>20:
        username=username[:20]

    while username in logged_usernames:
        connection.sendall("Username già presente nella stanza, riprovare:\n".encode())
        username=connection.recv(20).rstrip().decode()

    time="["+datetime.now().strftime("%H:%M")+"]"
    notify=time+"--> "+username+" è entrato nella stanza\n"

    if debug: 
        print(notify.rstrip(), address, sep=" ")
    if logging:
        log=open(path, "a")
        print(notify.rstrip(), address, sep=" ", file=log)
        log.close()

    for user in logged_usernames:
        users[user].sendall(notify.encode())

    logged_usernames.append(username)
    connection.sendall(b"Ok!\n")
    users[username]=connection
    
    try:
        while True:
            data = connection.recv(1024)
            if data:
                time="["+datetime.now().strftime("%H:%M")+"]"
                messaggio=time+username+": "+data.decode()

                if debug:
                    print(messaggio.rstrip(), address)  

                if logging:
                    log=open(path, "a")
                    print(messaggio.rstrip(), address, file=log) 
                    log.close() 

                for user in logged_usernames:
                    users[user].sendall(messaggio.encode())
            else:
                break    
    finally:
        time="["+datetime.now().strftime("%H:%M")+"]"
        notify=time+"<-- "+username+" è uscito dalla stanza\n"

        if debug: 
            print(notify.rstrip(), address)
        if logging:
            log=open(path, "a")
            print(notify.rstrip(), address, file=log)
            log.close()

        logged_usernames.remove(username)

        for user in logged_usernames:
            users[user].sendall(notify.encode())
        
        print(time+' Disconnected from:', address[1:-1])

        if logging:
            log=open(path, "a")
            print(time+' Disconnected from:', address[1:-1], file=log)
            log.close()
        logged_users-=1
        connection.close()
        users.pop(username)

def accept_connection(socket):
    client, address = socket.accept()
    if logged_users>MAX_CONNECTIONS:
        client.sendall(">Troppe connessioni\n".encode())
        client.close()
        return 

    address="("+address[0]+":"+str(address[1])+")"
    time="["+datetime.now().strftime("%H:%M")+"]"

    print(time+" Connected to: "+address[1:-1])

    if logging:
        log=open(path, "a")
        print(time+" Connected to: "+address[1:-1], file=log)
        log.close()

    start_new_thread(client_handler, (client, address)) 


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host,port))
socket.listen(MAX_CONNECTIONS)


while True:
   accept_connection(socket)