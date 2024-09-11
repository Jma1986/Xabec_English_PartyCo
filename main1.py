import tkinter as tk
import random
from tkinter import messagebox
import json

FONT = ("Terminal", 12)
players = []
scores = {}  # {"player1": 0, "player2": 0}
current_player_index = 0
question = ""
BACKGROUND_COLOR = "#263238"
BUTTON_BACKGROUND = "#90a4ae"

# Crear una instancia de la ventana principal
ventana = tk.Tk()

# Configurar propiedades de la ventana
ventana.title("Party&Co Game")
ventana.geometry("580x575")
ventana.config(bg=BACKGROUND_COLOR)

# cargar logos
imagen = tk.PhotoImage(file="logo3.png").subsample(2, 2)
button_roll_img = tk.PhotoImage(file="rolldice.png").subsample(4, 4)
button_correct_img = tk.PhotoImage(file="correct.png").subsample(4, 4)
button_incorrect_img = tk.PhotoImage(file="wrong.png").subsample(4, 4)

# Leer el archivo JSON y almacenar las listas en variables
with open("data.json", "r") as file:
    data = json.load(file)
    tools = data["tools"]
    verbs = data["verbs"]
    texts = data["texts"]
    modals = data["modals"]
# Funciones de inicio de juego

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
    else:
        messagebox.showwarning("Input Error", "Player name cannot be empty")
        
# widgets de inicio de juego

etiqueta_imagen = tk.Label(ventana, image=imagen, bg=BACKGROUND_COLOR)
etiqueta_imagen.grid(row=1, column=0, columnspan=2, padx=100, pady=20, sticky="ew")

entry = tk.Entry(ventana, font=FONT)
entry.grid(row=2, column=0, padx=50, pady=10, sticky="ew")

boton_new_player = tk.Button(ventana, text="New player", command=add_player, font=FONT, bg=BUTTON_BACKGROUND)
boton_new_player.grid(row=2, column=1, padx=50, pady=10, sticky="ew")

boton_start_game = tk.Button(ventana, text="Start game", command=start_game, font=FONT, bg=BUTTON_BACKGROUND)
boton_start_game.grid(row=3, column=0, padx=50, pady=10, columnspan=2, sticky="ew")

# Funciones del juego

def roll_die():
    global question
    roll = random.randint(1, 6)
    if roll == 1:
        question = "Speaking for 1 min."
    elif roll == 2:
        question = f"Tools: {random.choice(tools)}"
    elif roll == 3:
        question = f"Passive voice: {random.choice(verbs)}"
    elif roll == 4:
        question = f"Read and translate: {random.choice(texts)}"
    elif roll == 5:
        question = "Watch a movie fragment."
    else:
        question = f"Modal verbs: {random.choice(modals)}"
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

    label_player = tk.Label(ventana, text=f"{current_player}", font=("arial", 24, "bold"), bg=BACKGROUND_COLOR, fg="white")
    label_player.grid(row=0, column=0, padx=50, pady=30)

    button_roll = tk.Button(ventana, command=roll_die, image=button_roll_img , compound=tk.LEFT, bg=BUTTON_BACKGROUND)
    button_roll.grid(row=0, column=1, padx=100, pady=30, )

    label_question = tk.Label(ventana, text=question, font=("arial", 20), wraplength=500, bg=BACKGROUND_COLOR, fg="white")
    label_question.grid(row=1, column=0, columnspan=2, padx=50, pady=50)

    button_correct = tk.Button(ventana, command=correct_answer, image=button_correct_img, compound=tk.LEFT, bg=BUTTON_BACKGROUND)
    button_correct.grid(row=2, column=0, padx=100, pady=50)

    button_incorrect = tk.Button(ventana, command=next_player, image=button_incorrect_img, compound=tk.LEFT, bg=BUTTON_BACKGROUND)
    button_incorrect.grid(row=2, column=1, padx=100, pady=50)
    
    button_results = tk.Button(ventana, text="Print Results", command=print_results, font=FONT, bg=BUTTON_BACKGROUND)
    button_results.grid(row=3, column=0, padx=50, pady=50, columnspan=2, sticky="ew")


def correct_answer():
    global current_player_index
    current_player = players[current_player_index]
    scores[current_player] += 1
    messagebox.showinfo("Correct!", f"{current_player} scores! Total score: {scores[current_player]}")
    roll_die()

ventana.mainloop()