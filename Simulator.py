import random
import turtle
import tkinter as tk
from tkinter import ttk

# Function to generate random IPs
def random_IPS():
    first = random.randint(0, 255)
    second = random.randint(0, 255)
    third = random.randint(0, 255)
    fourth = random.randint(0, 255)
    return f"{first}.{second}.{third}.{fourth}"

# Initialize list of IPs
list_ip = [random_IPS() for _ in range(20)]

# Initialize target IP
target_ip = random.randint(0, len(list_ip) - 1)

# Initialize screen size
scsize = (500, 500)
screen = turtle.Screen()
screen.screensize(scsize[0], scsize[1])

# Initialize positions list
posList = []
for ip in list_ip:
    color = "black"
    pos = ((random.choice([-1, 1])) * (random.randint(50, scsize[0] - 50)),
           (random.choice([-1, 1])) *  random.randint(50, scsize[1] - 50))
    posList.append(pos)
    if list_ip.index(ip) == target_ip:
        color = "red"
    if list_ip.index(ip) == 0:
        color = "blue"
    turtle.penup()
    turtle.goto(pos[0], pos[1])
    turtle.pendown()
    turtle.dot(10, color)
    turtle.penup()
    turtle.goto(pos[0] - 50, pos[1] + 15)
    turtle.write(str(ip), font= ("Times New Roman", 15, "normal"))

turtle.penup()
turtle.goto(posList[0])

# Initialize black list IPs
black_list_ips = []

def virtualCircuit(nHops, log_text):
    hops = 0
    while True:
        ip = random.randint(0, len(list_ip) - 1)
        if ip in black_list_ips or ip == 0:
            continue
        if hops != nHops:
            turtle.goto(posList[ip])
            hops += 1
            log_text.insert(tk.END, f"{hops}\t{ip}\t{list_ip[ip]}\n")
            log_text.see(tk.END)
            black_list_ips.append(ip)
            if list_ip[ip] == list_ip[target_ip]:
                log_text.insert(tk.END, f"{list_ip[target_ip]} reached successfully.\n")
                break
        else:
            break

def datagram(nHops, nPackage, log_text):
    for p in range(nPackage):
        turtle.penup()
        turtle.goto(posList[0])
        turtle.pendown()
        hops = 0
        while True:
            ip = random.randint(0, len(list_ip) - 1)
            if ip in black_list_ips or ip == 0:
                continue
            if hops != nHops:
                turtle.goto(posList[ip])
                hops += 1
                log_text.insert(tk.END, f"{hops}\t{ip}\t{list_ip[ip]}\n")
                log_text.see(tk.END)
                black_list_ips.append(ip)
                if list_ip[ip] == list_ip[target_ip]:
                    log_text.insert(tk.END, f"{list_ip[target_ip]} reached successfully.\n")
                    black_list_ips.pop()
                    break
            else:
                break

def run_simulation():
    nHops = int(hops_entry.get())
    if mode_var.get() == "1":
        nPackage = int(package_entry.get())
        datagram(nHops, nPackage, log_text)
    else:
        virtualCircuit(nHops, log_text)

def close_application():
    screen.bye()
    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title("Network Simulation")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(mainframe, text="Mode:").grid(row=0, column=0, sticky=tk.W)
mode_var = tk.StringVar()
ttk.Radiobutton(mainframe, text="Datagram", variable=mode_var, value="1").grid(row=0, column=1, sticky=tk.W)
ttk.Radiobutton(mainframe, text="Virtual Circuit", variable=mode_var, value="2").grid(row=0, column=2, sticky=tk.W)

ttk.Label(mainframe, text="Number of Packages:").grid(row=1, column=0, sticky=tk.W)
package_entry = ttk.Entry(mainframe)
package_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Max Hops:").grid(row=2, column=0, sticky=tk.W)
hops_entry = ttk.Entry(mainframe)
hops_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Run Simulation", command=run_simulation).grid(row=3, column=0, columnspan=2)

log_text = tk.Text(mainframe, width=50, height=15)
log_text.grid(row=4, column=0, columnspan=3)

ttk.Button(mainframe, text="Close", command=close_application).grid(row=5, column=0, columnspan=3)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

mode_var.set("1")

root.mainloop()
turtle.done()
