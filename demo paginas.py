import requests

# Substitua pelo token de acesso do usuário obtido no fluxo de login
ACCESS_TOKEN = "COLOQUE_SEU_TOKEN_AQUI"

def listar_paginas(token):
    url = "https://graph.facebook.com/v23.0/me/accounts"
    params = {"access_token": token}
    response = requests.get(url, params=params)
    data = response.json()
    return data

if __name__ == "__main__":
    paginas = listar_paginas(ACCESS_TOKEN)
    print("📋 Lista de páginas administradas pelo usuário:")
    print(paginas)
