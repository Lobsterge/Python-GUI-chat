import socket
from _thread import *
import tkinter as tk
import tkinter.scrolledtext as st
import webbrowser
from tkinter.messagebox import showinfo
import re

check=False 
host="localhost" #modifica questi
port=4444 #modifica questi

def startup():
    global s
    global check
    if check==True:
        showinfo("Errore", "Sei già connesso")
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        output.insert("end", ">Il server non è raggiungibile\n")
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

def set_values(self=None):
    global host
    global port 
    global host_local
    global port_local
    global options
    
    if re.fullmatch("^\d+$", port_local.get())==None:
        showinfo("Errore", "Il numero della porta deve essere decimale")
        return

    host=host_local.get()
    port=int(port_local.get())
    options.destroy()

def configuration(self=None):
    global check
    global host
    global port 
    global host_local
    global port_local
    global options

    if check:
        showinfo("Errore", "Non puoi cambiare configurazione mentre sei connesso")
        return 

    host_local=tk.StringVar(value=host)
    port_local=tk.StringVar(value=str(port))
    
    
    options=tk.Toplevel(win)
    options.title("Config")
    options.wm_attributes("-topmost", True)
    options.lift()
    options.grab_set()
    padding=tk.Frame(options)
    padding2=tk.Frame(options)
    ip = tk.Label(master=padding, text="Host/IP:", height=1)
    ip_input= tk.Entry(master=padding, textvariable=host_local)
    port_text = tk.Label(master=padding2, text="Port:", height=1)
    port_input= tk.Entry(master=padding2, textvariable=port_local)

    ip.pack(anchor=tk.NW)
    ip_input.pack(anchor=tk.NW)
    port_text.pack(anchor=tk.NW)
    port_input.pack(anchor=tk.NW)
    padding.pack(padx=10, pady=10,anchor=tk.NW)
    padding2.pack(padx=10, pady=10,anchor=tk.NW)

    conferma = tk.Button(options, text="Conferma", command=set_values)
    options.bind("<Return>", set_values)
    options.geometry("165x175")
    options.minsize(165,176)
    options.maxsize(165,176)
    conferma.pack(pady=10)
    
    

win = tk.Tk()
win.title("Chat")

host_local=tk.StringVar(value=host)
port_local=tk.StringVar(value=str(port))
output = st.ScrolledText(win,width = 75, height = 16)
padding= tk.Frame()
paddingUP=tk.Frame()
status = tk.Label(master=padding, text="Non connesso", fg="red", height=1)
input = tk.Text(height=3)
send = tk.Button(text="Invia", width=10, height=1, command=send_data)
connect = tk.Button(master=padding, text="Connettiti", width=10, height=1, command=startup)
config = tk.Button(master=paddingUP, text="Configurazione", width=10, height=1, command=configuration)
help = tk.Button(master=paddingUP, text="Aiuto", width=10, height=1, command=open_link)



config.pack(side=tk.LEFT, anchor=tk.NW)  
help.pack(side=tk.LEFT, anchor=tk.NW)  
paddingUP.pack(anchor=tk.NW)
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