import json
import requests

dic = {}
json_file_path = "data_collection/irasutoya_kana_bis.json"

# Charge les données du JSON dans un dictionnaire
try:
    with open(json_file_path, 'r') as json_file:
        dic = json.load(json_file)
except FileNotFoundError:
    print("Le fichier JSON n'existe pas.")


images_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiHKwwhrrvSfSXe6rTZfiXsAKlGTK_qBUq2b4y6xrWeWibjP17AU9ztLvkBqt-Pn1qjosx-lZ7ybPRSiGUY0m2CA8RWiedULNX2r9Whj2LC7w6Q741i0VcJ554m950ugyVxz8SbYjX5cJDg/s72-c/souji_table_fuku_man.png"

img_data = requests.get(images_url).content

with open('netflix.jpg', 'wb') as handler: 

       handler.write(img_data) 