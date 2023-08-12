import socket
from _thread import *
import tkinter as tk
import tkinter.scrolledtext as st
import webbrowser
from tkinter.messagebox import showinfo

check=False 

def startup():
    global s
    global check
    if check==True:
        showinfo("Errore", "Sei già connesso")
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host="localhost" #modifica questi
    port=4444 #modifica questi

    try:
        s.connect((host,port))
    except:
        showinfo("Errore", "Non è stato possibile effettuare una connessione")
        return
    status.config(text="Connesso", fg="green")
    check=True
    start_new_thread(server_handler, (s, False))


def server_handler(connection, startup):
    try:
        while True:
            data = connection.recv(1024)
            if data:
                messaggio=data.decode()
                output.configure(state ='normal')
                fully_scrolled_down = output.yview()[1] == 1.0
                output.insert("end", messaggio)
                if fully_scrolled_down:
                    output.see("end")
                output.configure(state ='disabled')
            else:
                break    
    finally:
        connection.close()
        status.config(text="Non connesso", fg="red")
        output.configure(state ='normal')
        output.insert("end", ">Il server è stato spento, vai a picchiare chiunque lo stava hostando\n")
        global check
        check=False
        output.configure(state ='disabled')

def send_data(self=None):
    global check
    if check==False:
        showinfo("Errore", "Non sei connesso")
        return
    message=input.get("1.0", tk.END).rstrip().replace("\n", " ")
    input.delete("1.0", tk.END)
    try:
        if message.rstrip()!="":
            s.send((message+"\n").encode())
    except:
        showinfo("Errore", "Non mandare cose strane plz")

'''UI'''  

def open_link():
    webbrowser.open_new_tab("https://github.com/Lobsterge/Python-GUI-chat/tree/main")    

def scroll_up(self=None):
    output.yview_scroll(-1, "units")

def scroll_down(self=None):
    output.yview_scroll(1, "units")

win = tk.Tk()
win.title("Chat")

output = st.ScrolledText(win,width = 75, height = 16)
help = tk.Button(text="Aiuto", width=10, height=1, command=open_link)
padding= tk.Frame()
status = tk.Label(master=padding, text="Non connesso", fg="red", height=1)
input = tk.Text(height=3)
send = tk.Button(text="Invia", width=10, height=1, command=send_data)
connect = tk.Button(master=padding, text="Connettiti", width=10, height=1, command=startup)


help.pack(anchor=tk.NW)  
output.pack(fill=tk.BOTH, expand=True)
connect.pack(side=tk.LEFT, anchor=tk.W)
status.pack(side=tk.LEFT, anchor=tk.W)
padding.pack(anchor=tk.W)
input.pack(fill=tk.X)
send.pack(anchor=tk.SE)  


output.configure(state ='disabled')
win.bind("<Return>", send_data)
win.bind("<KP_Up>", scroll_up)
win.bind("<KP_Down>",scroll_down)
win.bind("<Up>", scroll_up)
win.bind("<Down>",scroll_down)
win.mainloop()  