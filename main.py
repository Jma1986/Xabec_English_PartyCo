import tkinter as tk
import random
from tkinter import messagebox
import csv

FONT = ("arial", 12)
players = []
scores = {}  # {"player1": 0, "player2": 0}
current_player_index = 0
question = ""

# Crear una instancia de la ventana principal
ventana = tk.Tk()

# Configurar propiedades de la ventana
ventana.title("Party&Co Game")
ventana.geometry("600x500")

# Agregar widgets a la ventana
imagen = tk.PhotoImage(file="logo3.png")
imagen = imagen.subsample(2, 2)
etiqueta_imagen = tk.Label(ventana, image=imagen)
etiqueta_imagen.grid(row=1, column=0, columnspan=2, padx=100, pady=20)

def start_game():
    etiqueta_imagen.grid_forget()
    entry.grid_forget()
    boton_new_player.grid_forget()
    boton_start_game.grid_forget()
    update_game()

def add_player():
    player_name = entry.get()
    if player_name:
        players.append(player_name)
        scores[player_name] = 0
        entry.delete(0, tk.END)
        print(players)
    else:
        messagebox.showwarning("Input Error", "Player name cannot be empty")

entry = tk.Entry(ventana, font=FONT)
entry.grid(row=2, column=0, padx=10, pady=10)

boton_new_player = tk.Button(ventana, text="New player", command=add_player)
boton_new_player.grid(row=2, column=1, padx=5, pady=10)

boton_start_game = tk.Button(ventana, text="Start game", command=start_game)
boton_start_game.grid(row=3, column=0, padx=5, pady=10, columnspan=2)

# Cargar la imagen del botón "Roll Dice"
button_roll_img = tk.PhotoImage(file="rolldice.png").subsample(4, 4)
button_correct_img = tk.PhotoImage(file="correct.png").subsample(4, 4)
button_incorrect_img = tk.PhotoImage(file="wrong.png").subsample(4, 4)

def roll_die():
    global question
    roll = random.randint(1, 6)
    if roll == 1:
        question = "Talk 1 min about yourself."
    elif roll == 2:
        tools = ["hammer", "screwdriver", "wrench", "pliers", "saw", "drill", "tape measure", "level", "soldering iron", "file", "paintbrush", "ladder", "shovel", "safety glasses", "earmuffs", "grinder", "sandpaper", "hex keys", "nail gun", "multimeter", "nail", "screw", "bolt", "nut", "axe"]
        question = f"use the following tool in a sentence and translate it: {random.choice(tools)}"
    elif roll == 3:
        verbs = ["The mechanic repairs the car.", "The technician fixes the computer.", "She installs the new software.", "He checks the engine every day.", "They clean the workshop.", 
"The mechanic repaired the car.", "The technician fixed the computer yesterday.", "She installed the new software last week.", "He checked the engine yesterday.", "They cleaned the workshop last night.", 
"The mechanic is repairing the car.", "The technician is fixing the computer right now.", "She is installing the new software.", "He is checking the engine.", "They are cleaning the workshop now.", 
"The mechanic was repairing the car.", "The technician was fixing the computer when I arrived.", "She was installing the new software.", "He was checking the engine.", "They were cleaning the workshop.", 
"The mechanic will repair the car tomorrow.", "The technician will fix the computer later.", "She will install the new software soon.", "He will check the engine next week.", "They will clean the workshop tomorrow."]
        question = f"Trasnform the following sentence into passive voice: {random.choice(verbs)}"
    elif roll == 4:
        texts = ["The motor is running fast.", "Turn off the switch, please.", "The wires are connected here.", "We need a new battery.", "This tool is called a wrench.", "The fan is not working.", "I will fix the machine.", "Check the voltage first.", "The circuit is open.", "We need more screws.", "This part is broken.", "I need to replace the fuse.", "The engine makes a strange noise.", "This wire is too short.", "The light is flickering.", "Can you hand me the pliers?", "The current flows through the cable.", "We must adjust the settings.", "The pump stopped working.", "Tighten the bolts, please.", "The switch is on the right.", "The tool box is under the table.", "This machine needs oil.", "The belt is loose.", "Don’t forget to wear safety gloves.", "The motor is overheating.", "I will install the new circuit.", "The fan is making noise.", "We need to replace the wires.", "The tool is in the drawer.", "Is the voltage correct?", "The battery is fully charged.", "The circuit breaker tripped.", "The light bulb needs to be changed.", "I will unplug the machine.", "Check the fuse box.", "The power cable is damaged.", "This is the main control panel.", "The rotor is spinning slowly.", "The multimeter shows low voltage.", "Connect the red wire to the terminal.", "We need to lubricate the gears.", "The sensor is malfunctioning.", "The generator produces electricity.", "The fan blades are dirty.", "I need to tighten this screw.", "The machine is vibrating too much.", "This is an electric drill.", "The voltage is too high.", "The pump needs to be cleaned.", "The socket is loose."]
        question = f"Read and translate: {random.choice(texts)}"
    elif roll == 5:
        question = "Watch a movie fragment and translate it."
    else:
        modals = ["can", "could", "may", "might", "will", "would", "shall", "should", "must", "ought to"]
        question = f"Use the following modal verb in a sentence and tranlate it: {random.choice(modals)}"
    update_game()

def next_player():
    global current_player_index
    current_player_index += 1
    if current_player_index >= len(players):
        current_player_index = 0
    update_game()
    
def print_results():
    result_text = "Results:\n"
    for player, score in scores.items():
        result_text += f"{player}: {score}\n"
    messagebox.showinfo("Results", result_text)
    
    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Player", "Score"])
        for player, score in scores.items():
            writer.writerow([player, score])
    messagebox.showinfo("CSV Downloaded", "Results saved as results.csv")

def update_game():
    global current_player_index
    current_player = players[current_player_index]

    for widget in ventana.winfo_children():
        widget.grid_forget()

    label_player = tk.Label(ventana, text=f"Player: {current_player}", font=FONT)
    label_player.grid(row=0, column=0, padx=5, pady=10)

    button_roll = tk.Button(ventana, command=roll_die, image=button_roll_img , compound=tk.LEFT)
    button_roll.grid(row=0, column=1, padx=5, pady=10, )

    label_question = tk.Label(ventana, text=question, font=("arial", 20))
    label_question.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    button_correct = tk.Button(ventana, command=correct_answer, image=button_correct_img, compound=tk.LEFT)
    button_correct.grid(row=2, column=0, padx=5, pady=10)

    button_incorrect = tk.Button(ventana, command=next_player, image=button_incorrect_img, compound=tk.LEFT)
    button_incorrect.grid(row=2, column=1, padx=5, pady=10)
    
    button_results = tk.Button(ventana, text="Print Results", command=print_results)
    button_results.grid(row=3, column=0, padx=5, pady=10, columnspan=2)


   

def correct_answer():
    global current_player_index
    current_player = players[current_player_index]
    scores[current_player] += 1
    messagebox.showinfo("Correct!", f"{current_player} scores! Total score: {scores[current_player]}")
    roll_die()

ventana.mainloop()