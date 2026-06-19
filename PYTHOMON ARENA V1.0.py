import tkinter as tk
from PIL import Image, ImageTk
import random
import requests
import pygame

# =========================
# AUDIO
# =========================

pygame.mixer.init()

def play_music(file, loop=True):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1 if loop else 0)

def play_sfx(file):
    pygame.mixer.Sound(file).play()

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

def go_select():
    play_sfx("sounds/attack.wav")
    show(select)

tk.Button(menu, text="JOGAR", font=("Arial", 20), command=go_select).pack()

play_music("sounds/menu.mp3")

# =========================
# SELEÇÃO
# =========================

set_bg(select)

tk.Label(select, text="ESCOLHE OS TEUS POKÉMONS", font=("Arial", 22, "bold"), bg="white").pack(pady=10)

frame_select_ui = tk.Frame(select, bg="white")
frame_select_ui.pack(pady=30)

pokemon_j1 = tk.StringVar(value="Bulbasaur")
pokemon_j2 = tk.StringVar(value="Charmander")

card1 = tk.Frame(frame_select_ui, bg="#ffcccc", width=300, height=300)
card1.grid(row=0, column=0, padx=30)

tk.Label(card1, text="Jogador 1", bg="#ffcccc", font=("Arial", 14, "bold")).pack(pady=10)
tk.OptionMenu(card1, pokemon_j1, *coordenadas.keys()).pack()

tk.Label(card1, text="VS", bg="#ffcccc", font=("Arial", 16, "bold")).pack(pady=20)

card2 = tk.Frame(frame_select_ui, bg="#ccccff", width=300, height=300)
card2.grid(row=0, column=1, padx=30)

tk.Label(card2, text="Jogador 2", bg="#ccccff", font=("Arial", 14, "bold")).pack(pady=10)
tk.OptionMenu(card2, pokemon_j2, *coordenadas.keys()).pack()

def start_game():
    global pokemon1, pokemon2, vida1, vida2

    play_music("sounds/battle.mp3")

    pokemon1 = criar_pokemon(pokemon_j1.get())
    pokemon2 = criar_pokemon(pokemon_j2.get())

    vida1 = pokemon1["vida"]
    vida2 = pokemon2["vida"]

    load_battle()
    show(battle)

tk.Button(select, text="COMEÇAR BATALHA", command=start_game, font=("Arial", 16)).pack(pady=20)

# =========================
# BATTLE UI
# =========================

set_bg(battle)

frame_left = tk.Frame(battle, bg="#ffdddd")
frame_left.pack(side="left", fill="both", expand=True)

frame_right = tk.Frame(battle, bg="#ddddff")
frame_right.pack(side="right", fill="both", expand=True)

img_j1 = tk.Label(frame_left)
img_j1.pack(pady=10)

img_j2 = tk.Label(frame_right)
img_j2.pack(pady=10)

label_j1 = tk.Label(frame_left, font=("Arial", 14))
label_j1.pack()

label_j2 = tk.Label(frame_right, font=("Arial", 14))
label_j2.pack()

turn_label = tk.Label(battle, font=("Arial", 16), bg="white")
turn_label.place(x=350, y=10)

def load_sprite(poke_id):
    img = Image.open(requests.get(sprite_url(poke_id), stream=True).raw)
    img = img.resize((150, 150))
    return ImageTk.PhotoImage(img)

def load_battle():
    global sprite1, sprite2

    sprite1 = load_sprite(pokemon1["id"])
    sprite2 = load_sprite(pokemon2["id"])

    img_j1.config(image=sprite1)
    img_j2.config(image=sprite2)

    update_ui()

def update_ui():
    label_j1.config(text=f"{pokemon1['nome']} HP: {vida1}")
    label_j2.config(text=f"{pokemon2['nome']} HP: {vida2}")
    turn_label.config(text=f"Turno: {turno}")

# =========================
# ATAQUES + DEFESA
# =========================

def attack1_skill1():
    global vida2, turno, def2
    if turno != 1: return

    play_sfx("sounds/attack.wav")
    dmg = random.randint(12, 20)

    if def2:
        dmg //= 2
        def2 = False

    vida2 -= dmg
    turno = 2
    check_win()
    update_ui()

def attack1_skill2():
    global vida2, turno, def2
    if turno != 1: return

    play_sfx("sounds/attack.wav")
    dmg = random.randint(8, 25)

    if def2:
        dmg //= 2
        def2 = False

    vida2 -= dmg
    turno = 2
    check_win()
    update_ui()

def defend1():
    global def1, turno
    if turno == 1:
        def1 = True
        turno = 2
        update_ui()

def attack2_skill1():
    global vida1, turno, def1
    if turno != 2: return

    play_sfx("sounds/attack.wav")
    dmg = random.randint(12, 20)

    if def1:
        dmg //= 2
        def1 = False

    vida1 -= dmg
    turno = 1
    check_win()
    update_ui()

def attack2_skill2():
    global vida1, turno, def1
    if turno != 2: return

    play_sfx("sounds/attack.wav")
    dmg = random.randint(8, 25)

    if def1:
        dmg //= 2
        def1 = False

    vida1 -= dmg
    turno = 1
    check_win()
    update_ui()

def defend2():
    global def2, turno
    if turno == 2:
        def2 = True
        turno = 1
        update_ui()

def check_win():
    if vida1 <= 0:
        play_sfx("sounds/win.wav")
        winner_text.config(text=f"{pokemon2['nome']} venceu!")
        show(result)

    if vida2 <= 0:
        play_sfx("sounds/win.wav")
        winner_text.config(text=f"{pokemon1['nome']} venceu!")
        show(result)

# =========================
# BOTÕES
# =========================

tk.Label(frame_left, text="Ações").pack()

tk.Button(frame_left, text="Skill 1", command=attack1_skill1).pack()
tk.Button(frame_left, text="Skill 2", command=attack1_skill2).pack()
tk.Button(frame_left, text="Defender", command=defend1).pack()

tk.Label(frame_right, text="Ações").pack()

tk.Button(frame_right, text="Skill 1", command=attack2_skill1).pack()
tk.Button(frame_right, text="Skill 2", command=attack2_skill2).pack()
tk.Button(frame_right, text="Defender", command=defend2).pack()

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