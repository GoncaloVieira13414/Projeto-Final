import requests, os

url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"

def poke_search():
    global url

    b = requests.get(url).json()
    
    with open("id.txt", "w") as my_file:

        for x in range(0,30):
            c = b["results"][x]["url"]
            a = b["results"][x]["name"]
            my_file.write(a + ";")
            d = requests.get(c).json()

            for y in range(0, 1):
                f = d["abilities"][0]["ability"]["name"]
                g = d["abilities"][1]["ability"]["name"]
                my_file.write(f + ";"+ g + ";" + "\n")
       
       
            
poke_search()