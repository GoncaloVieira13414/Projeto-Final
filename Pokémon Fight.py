import tkinter as tk
from PIL import Image, ImageTk
import requests, os

url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"


def mudar_para_janela(janela_alvo):
    # Esconde todos os ecrãs/frames
    frame_principal.pack_forget()
    frame_selecao.pack_forget()
    frame_batalha.pack_forget()
    frame_resultados.pack_forget()
    
    # Mostra apenas o ecrã que queremos
    janela_alvo.pack(fill="both", expand=True)



# def poke_search():
#     global url

#     b = requests.get(url).json()
    
#     with open("id.txt", "w") as my_file:

#         for x in range(0,30):
#             c = b["results"][x]["url"]
#             a = b["results"][x]["name"]
#             my_file.write(a + ";")
#             d = requests.get(c).json()

#             for y in range(0, 1):
#                 f = d["abilities"][0]["ability"]["name"]
#                 g = d["abilities"][1]["ability"]["name"]
#                 my_file.write(f + ";"+ g + ";" + "\n")
            
# poke_search()







root = tk.Tk()
root.title("Pythomon: Arena")
root.geometry("800x600")

pokemon_j1 = tk.StringVar()
pokemon_j1.set("Bulbasaur")

pokemon_j2 = tk.StringVar()
pokemon_j2.set("Bulbasaur")

escolha_j1 = pokemon_j1.get()
escolha_j2 = pokemon_j2.get()

print(escolha_j1)
print(escolha_j2)
coordenadas = {
    "Pikachu": {
        id:1
    },
    "BUbasar":{
        id:2
    }
}







# MENU PRINCIPAL(WINDOW 1)

imagem = Image.open(r"C:\Users\Joao Duarte\PycharmProjects\GVPython\poke_background.jpeg")
imagem = imagem.resize((800, 600))
foto = ImageTk.PhotoImage(imagem)

frame_principal = tk.Frame(root)
frame_principal.pack(fill="both", expand=True)

fundo = tk.Label(frame_principal, image=foto)
fundo.place(x=0, y=0, relwidth=1, relheight=1)

label_titulo = tk.Label(frame_principal, text="Pythomon: Arena", font=("Arial", 30, "bold"), bg="#fff3cd")
label_titulo.pack(pady=50)

# Botão que leva-me a window 2
btn_jogar = tk.Button(frame_principal, text="Jogar", font=("Arial", 25), command=lambda: mudar_para_janela(frame_selecao))
btn_jogar.pack(pady=100)


# SELEÇÃO DOS PERSONAGENS (WINDOW 2)
frame_selecao = tk.Frame(root)

fundo = tk.Label(frame_selecao, image=foto)
fundo.place(x=0, y=0, relwidth=1, relheight=1)


tk.Label(frame_selecao, text="Escolha os Pokémon", font=("Arial", 20, "bold")).pack(pady=10)


tk.Label(frame_selecao, text="VS", font=("Arial", 25, "bold")).pack(pady=10)

# Zona de seleção
frame_pokemons = tk.Frame(frame_selecao)
frame_pokemons.pack(pady=20)

# J1(ESQUERDA)
frame_j1 = tk.Frame(frame_pokemons)
frame_j1.pack(side="left", padx=10)

tk.Label(frame_j1, text="Jogador 1").grid(row=0,column=0,padx=10, pady=10,sticky="w")

opcoes = tk.OptionMenu(frame_j1, pokemon_j1, coordenadas)
opcoes.grid(row=1, column=0, padx=10,pady=5,sticky="w")


# J2(DIREITA)
frame_j2 = tk.Frame(frame_pokemons)
frame_j2.pack(side="left", padx=10)

tk.Label(frame_j2, text="Jogador 2").grid(row=0,column=0,padx=10, pady=10,sticky="w")

opcoes2 = tk.OptionMenu(frame_j2, pokemon_j2, *coordenadas.keys())
opcoes2.grid(row=1, column=0, padx=10,pady=5,sticky="w")

# botão para ir para a window 3
btn_confirmar = tk.Button(frame_selecao, text="Confirmar Seleção", font=("Arial", 14), command=lambda: mudar_para_janela(frame_batalha))
btn_confirmar.pack(pady=20)


# BATALHA PYTHOMONS (3)
frame_batalha = tk.Frame(root, bg="#fff3cd")

fundo = tk.Label(frame_batalha, image=foto)
fundo.place(x=0, y=0, relwidth=1, relheight=1)

label_bat = tk.Label(frame_batalha, text="Arena de Batalha", font=("Arial", 24), bg="#fff3cd")
label_bat.pack(pady=20)

frame_split_bat = tk.Frame(frame_batalha, bg="#fff3cd")
frame_split_bat.pack(fill="both", expand=True, pady=10)

f_bat_j1 = tk.Frame(frame_split_bat, bg="#f8d7da")
f_bat_j1.pack(side="left", fill="both", expand=True, padx=10, pady=10)
tk.Label(f_bat_j1, text="Ecrã J1", bg="#f8d7da").pack(pady=10)
tk.Label(f_bat_j1, text="Habilidades J1", bg="#f8d7da").pack(side="bottom", pady=10)


f_bat_j2 = tk.Frame(frame_split_bat, bg="#cfe2ff")
f_bat_j2.pack(side="right", fill="both", expand=True, padx=10, pady=10)
tk.Label(f_bat_j2, text="Ecrã J2", bg="#cfe2ff").pack(pady=10)
tk.Label(f_bat_j2, text="Habilidades J2", bg="#cfe2ff").pack(side="bottom", pady=10)

# Botão para a tela de resultados
btn_Terminar = tk.Button(frame_batalha, text="Finalizar Batalha", font=("Arial", 14), command=lambda: mudar_para_janela(frame_resultados))
btn_Terminar.pack(pady=20)


# RESULTADOS (4)
frame_resultados = tk.Frame(root, bg="#e2e3e5")

fundo = tk.Label(frame_resultados, image=foto)
fundo.place(x=0, y=0, relwidth=1, relheight=1)

label_res = tk.Label(frame_resultados, text="Resultados Finais", font=("Arial", 24), bg="#e2e3e5")
label_res.pack(pady=50)

label_vencedor = tk.Label(frame_resultados, text="O Vencedor é...", font=("Arial", 18, "italic"), bg="#e2e3e5")
label_vencedor.pack(pady=20)

# voltar ao menu (Window 1)
btn_reiniciar = tk.Button(frame_resultados, text="Voltar ao Menu Principal", font=("Arial", 14), command=lambda: mudar_para_janela(frame_principal))
btn_reiniciar.pack(pady=20)



frame_principal.pack(fill="both", expand=True)

root.mainloop()