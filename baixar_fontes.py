import os
import requests

os.makedirs("resources/fonts", exist_ok=True)

urls = {
    "Roboto-Bold.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf",
    "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
}

for nome, url in urls.items():
    caminho = os.path.join("resources", "fonts", nome)
    print(f"Baixando {nome}...")
    r = requests.get(url)
    with open(caminho, "wb") as f:
        f.write(r.content)
print("Fontes baixadas com sucesso.")
