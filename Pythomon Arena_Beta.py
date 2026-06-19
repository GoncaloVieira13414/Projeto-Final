import tkinter as tk
from PIL import Image, ImageTk
import random
import requests

# =========================
# POKÉMONS
# =========================

coordenadas = {
    "Bulbasaur": {"id": 1, "habilidade1": "overgrow", "habilidade2": "chlorophyll"},
    "Charmander": {"id": 4, "habilidade1": "blaze", "habilidade2": "solar-power"},
    "Squirtle": {"id": 7, "habilidade1": "torrent", "habilidade2": "rain-dish"},
    "Pikachu": {"id": 25, "habilidade1": "static", "habilidade2": "lightning-rod"},
    "Charizard": {"id": 6, "habilidade1": "blaze", "habilidade2": "solar-power"},
    "Blastoise": {"id": 9, "habilidade1": "torrent", "habilidade2": "rain-dish"}
}

def criar_pokemon(nome):
    base = coordenadas[nome]
    return {
        "id": base["id"],
        "nome": nome,
        "habilidade1": base["habilidade1"],
        "habilidade2": base["habilidade2"],
        "vida": random.randint(100, 150),
        "dano": random.randint(10, 25)
    }

def sprite_url(poke_id):
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{poke_id}.png"

# =========================
# GAME STATE
# =========================

pokemon1 = None
pokemon2 = None

vida1 = 0
vida2 = 0

turno = 1
def1 = False
def2 = False

# =========================
# WINDOW
# =========================

root = tk.Tk()
root.title("Pythomon Arena")
root.geometry("900x600")

# =========================
# BACKGROUND
# =========================

bg_img = Image.open(r"C:\Users\shark\PycharmProjects\GVPYTHON\Módulo 2\Projeto Final\poke_background.jpeg")
bg_img = bg_img.resize((900, 600))
bg_photo = ImageTk.PhotoImage(bg_img)

def set_bg(frame):
    bg = tk.Label(frame, image=bg_photo)
    bg.place(x=0, y=0, relwidth=1, relheight=1)

# =========================
# FRAMES
# =========================

menu = tk.Frame(root)
select = tk.Frame(root)
battle = tk.Frame(root)
result = tk.Frame(root)

for f in (menu, select, battle, result):
    f.place(relwidth=1, relheight=1)

def show(frame):
    frame.tkraise()

# =========================
# MENU
# =========================

set_bg(menu)

tk.Label(menu, text="PYTHOMON ARENA", font=("Arial", 30, "bold"), bg="white").pack(pady=50)
tk.Button(menu, text="JOGAR", font=("Arial", 20), command=lambda: show(select)).pack()

# =========================
# SELEÇÃO
# =========================

pokemon_j1 = tk.StringVar(value="Bulbasaur")
pokemon_j2 = tk.StringVar(value="Charmander")

set_bg(select)

tk.Label(select, text="Jogador 1", bg="white").pack()
tk.OptionMenu(select, pokemon_j1, *coordenadas.keys()).pack()

tk.Label(select, text="Jogador 2", bg="white").pack()
tk.OptionMenu(select, pokemon_j2, *coordenadas.keys()).pack()

# =========================
# BATALHA UI
# =========================

set_bg(battle)

frame_left = tk.Frame(battle, bg="#ffcccc", width=450, height=600)
frame_left.pack(side="left", fill="both", expand=True)

frame_right = tk.Frame(battle, bg="#ccccff", width=450, height=600)
frame_right.pack(side="right", fill="both", expand=True)

img_j1 = tk.Label(frame_left)
img_j1.pack(pady=20)

img_j2 = tk.Label(frame_right)
img_j2.pack(pady=20)

label_j1 = tk.Label(frame_left, font=("Arial", 14), bg="#ffcccc")
label_j1.pack()

label_j2 = tk.Label(frame_right, font=("Arial", 14), bg="#ccccff")
label_j2.pack()

turn_label = tk.Label(battle, font=("Arial", 16), bg="white")
turn_label.place(x=350, y=10)

# =========================
# LOAD SPRITES
# =========================

def load_sprite(poke_id):
    url = sprite_url(poke_id)
    img = Image.open(requests.get(url, stream=True).raw)
    img = img.resize((150, 150))
    return ImageTk.PhotoImage(img)

# =========================
# UPDATE UI
# =========================

def update_ui():
    global img1_ref, img2_ref

    label_j1.config(text=f"{pokemon1['nome']} HP: {vida1}")
    label_j2.config(text=f"{pokemon2['nome']} HP: {vida2}")

    turn_label.config(text=f"Turno: Jogador {turno}")

# =========================
# GAME START
# =========================

def start_game():
    global pokemon1, pokemon2, vida1, vida2
    global img1_ref, img2_ref, sprite1, sprite2

    pokemon1 = criar_pokemon(pokemon_j1.get())
    pokemon2 = criar_pokemon(pokemon_j2.get())

    vida1 = pokemon1["vida"]
    vida2 = pokemon2["vida"]

    sprite1 = load_sprite(pokemon1["id"])
    sprite2 = load_sprite(pokemon2["id"])

    img_j1.config(image=sprite1)
    img_j2.config(image=sprite2)

    update_ui()
    show(battle)

tk.Button(select, text="COMEÇAR", command=start_game).pack()

# =========================
# COMBAT
# =========================

def attack1():
    global vida2, turno, def2

    if turno != 1:
        return

    dmg = random.randint(pokemon1["dano"]-5, pokemon1["dano"]+5)

    if def2:
        dmg //= 2
        def2 = False

    vida2 -= dmg
    turno = 2

    check_win()
    update_ui()

def attack2():
    global vida1, turno, def1

    if turno != 2:
        return

    dmg = random.randint(pokemon2["dano"]-5, pokemon2["dano"]+5)

    if def1:
        dmg //= 2
        def1 = False

    vida1 -= dmg
    turno = 1

    check_win()
    update_ui()

def defend1():
    global def1, turno
    if turno == 1:
        def1 = True
        turno = 2
        update_ui()

def defend2():
    global def2, turno
    if turno == 2:
        def2 = True
        turno = 1
        update_ui()

def check_win():
    global winner_text

    if vida1 <= 0:
        winner_text.config(text=f"{pokemon2['nome']} venceu!")
        show(result)

    if vida2 <= 0:
        winner_text.config(text=f"{pokemon1['nome']} venceu!")
        show(result)

# =========================
# BATTLE BUTTONS
# =========================

tk.Button(frame_left, text="ATACAR", command=attack1).pack(pady=5)
tk.Button(frame_left, text="DEFENDER", command=defend1).pack(pady=5)

tk.Button(frame_right, text="ATACAR", command=attack2).pack(pady=5)
tk.Button(frame_right, text="DEFENDER", command=defend2).pack(pady=5)

# =========================
# RESULT
# =========================

winner_text = tk.Label(result, font=("Arial", 20), bg="white")
winner_text.pack(pady=200)

tk.Button(result, text="MENU", command=lambda: show(menu)).pack()

# =========================
# START
# =========================

show(menu)
root.mainloop()